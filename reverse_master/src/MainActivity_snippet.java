// Extract from MainActivity.onClick - first-half XOR check
final byte[] key = new byte[]{66,51,122,33,86};
final byte[] enc = new byte[]{122,86,27,22,53,35,80,77,24,98,122,7,72,21,98,114};
byte[] out = new byte[16];
for (int i = 0; i < 16; i++) out[i] = (byte)(enc[i] ^ key[i % key.length]);
String firstHalf = new String(out, java.nio.charset.StandardCharsets.UTF_8);
// -> "8ea7cac794842440"
