<?php
/**
 * Index page for Vertex Contact Form Service
 */
header('Content-Type: application/json');

echo json_encode([
    'service' => 'Vertex Experience Contact Form',
    'version' => '1.0.0',
    'status' => 'running',
    'endpoints' => [
        'POST /contact-form-handler.php' => 'Submit contact form',
        'GET /health.php' => 'Health check'
    ]
]);
