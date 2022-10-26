<?php
function encrypt($texto)
{
  $key = '';  // Una clave de codificacion, debe usarse la misma para encriptar y desencriptar
  $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length('aes-256-cbc'));
  $encrypted = openssl_encrypt($texto, 'aes-256-cbc', $key, 0, $iv);
  return base64_encode($encrypted . '::' . $iv);
}

function decrypt($texto)
{
  $key = '';
  list($encrypted_data, $iv) = explode('::', base64_decode($texto), 2);
  return openssl_decrypt($encrypted_data, 'aes-256-cbc', $key, 0, $iv);
}

$file = 'data.txt';
$pathname = dirname(__FILE__);
$filepath = $pathname . '\\' . $file;
$response = [];
if (file_exists($filepath)) {
  $string = file_get_contents($filepath);
  $objData = json_decode($string);

  $response['data'] = $objData->data;
  $response['option'] = $objData->option;

  if ($objData->option == 2) {
    $response['encrypted'] = encrypt($objData->data);
  } elseif ($objData->option == 1) {
    $response['decrypted'] = decrypt($objData->data);
  }
} else {
  $response['error'] = 'No existe el archivo';
}
echo json_encode($response);
