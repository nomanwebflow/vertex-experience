<?php
/**
 * Contact Form Handler for Vertex Experience
 * Handles form submissions from free-audit.html
 * Deployed on Google Cloud Run
 */

// Enable error reporting for debugging (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);

// CORS headers for cross-origin requests
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit();
}

// Load Composer autoloader
require_once __DIR__ . '/vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// Get environment variables
$smtpHost = getenv('SMTP_HOST') ?: 'smtp.gmail.com';
$smtpPort = getenv('SMTP_PORT') ?: 587;
$smtpUsername = getenv('SMTP_USERNAME');
$smtpPassword = getenv('SMTP_PASSWORD');
$recipientEmail = getenv('RECIPIENT_EMAIL');
$redirectUrl = getenv('REDIRECT_URL') ?: 'https://vertexexperience.com/thank-you';

// Validate environment variables
if (!$smtpUsername || !$smtpPassword || !$recipientEmail) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Server configuration error. Please contact the administrator.'
    ]);
    error_log('Missing required environment variables: SMTP_USERNAME, SMTP_PASSWORD, or RECIPIENT_EMAIL');
    exit();
}

// Get POST data (support both form-data and JSON)
$contentType = $_SERVER['CONTENT_TYPE'] ?? '';
if (strpos($contentType, 'application/json') !== false) {
    $input = json_decode(file_get_contents('php://input'), true);
} else {
    $input = $_POST;
}

// Honeypot spam protection
if (!empty($input['botcheck'])) {
    // Bot detected, pretend success but don't send email
    echo json_encode([
        'success' => true,
        'message' => 'Thank you for your submission!'
    ]);
    exit();
}

// Validate required fields
$errors = [];

$name = trim($input['name'] ?? '');
if (empty($name)) {
    $errors[] = 'Name is required';
}

$email = trim($input['email'] ?? '');
if (empty($email)) {
    $errors[] = 'Email is required';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Invalid email address';
}

$websiteLink = trim($input['Website-Link'] ?? '');
if (empty($websiteLink)) {
    $errors[] = 'Website URL is required';
}

$message = trim($input['message'] ?? '');
if (empty($message)) {
    $errors[] = 'Message is required';
}

// Optional fields
$howDidYouHear = trim($input['How-did-you-hear-from-us'] ?? 'Not specified');
$privacyPolicy = !empty($input['Privacy-Policy']);

if (!$privacyPolicy) {
    $errors[] = 'You must accept the privacy policy';
}

// Return validation errors
if (!empty($errors)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => 'Validation failed',
        'errors' => $errors
    ]);
    exit();
}

// Sanitize inputs
$name = htmlspecialchars($name, ENT_QUOTES, 'UTF-8');
$email = htmlspecialchars($email, ENT_QUOTES, 'UTF-8');
$websiteLink = htmlspecialchars($websiteLink, ENT_QUOTES, 'UTF-8');
$message = htmlspecialchars($message, ENT_QUOTES, 'UTF-8');
$howDidYouHear = htmlspecialchars($howDidYouHear, ENT_QUOTES, 'UTF-8');

// Create PHPMailer instance
$mail = new PHPMailer(true);

try {
    // Server settings
    $mail->isSMTP();
    $mail->Host = $smtpHost;
    $mail->SMTPAuth = true;
    $mail->Username = $smtpUsername;
    $mail->Password = $smtpPassword;
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail->Port = $smtpPort;
    
    // Recipients
    $mail->setFrom($smtpUsername, 'Vertex Experience Contact Form');
    $mail->addAddress($recipientEmail);
    $mail->addReplyTo($email, $name);
    
    // Content
    $mail->isHTML(true);
    $mail->Subject = "New Free Audit Request from {$name}";
    
    // Email body
    $emailBody = "
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #4d65ff; color: white; padding: 20px; text-align: center; }
            .content { background-color: #f9f9f9; padding: 20px; }
            .field { margin-bottom: 15px; }
            .label { font-weight: bold; color: #555; }
            .value { margin-top: 5px; padding: 10px; background-color: white; border-left: 3px solid #4d65ff; }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h2>New Free Audit Request</h2>
            </div>
            <div class='content'>
                <div class='field'>
                    <div class='label'>Name:</div>
                    <div class='value'>{$name}</div>
                </div>
                <div class='field'>
                    <div class='label'>Email:</div>
                    <div class='value'>{$email}</div>
                </div>
                <div class='field'>
                    <div class='label'>Website URL:</div>
                    <div class='value'><a href='{$websiteLink}'>{$websiteLink}</a></div>
                </div>
                <div class='field'>
                    <div class='label'>How did you hear from us:</div>
                    <div class='value'>{$howDidYouHear}</div>
                </div>
                <div class='field'>
                    <div class='label'>Message:</div>
                    <div class='value'>{$message}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ";
    
    $mail->Body = $emailBody;
    $mail->AltBody = "New Free Audit Request\n\n" .
                     "Name: {$name}\n" .
                     "Email: {$email}\n" .
                     "Website URL: {$websiteLink}\n" .
                     "How did you hear from us: {$howDidYouHear}\n\n" .
                     "Message:\n{$message}";
    
    // Send email
    $mail->send();
    
    // Success response
    echo json_encode([
        'success' => true,
        'message' => 'Thank you for your submission! We will get back to you soon.',
        'redirect' => $redirectUrl
    ]);
    
} catch (Exception $e) {
    error_log("Email sending failed: {$mail->ErrorInfo}");
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Failed to send email. Please try again later.'
    ]);
}
