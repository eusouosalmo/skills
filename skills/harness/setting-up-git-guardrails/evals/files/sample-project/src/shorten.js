const ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789";

export function shorten(id) {
  let out = "";
  do {
    out = ALPHABET[id % ALPHABET.length] + out;
    id = Math.floor(id / ALPHABET.length);
  } while (id > 0);
  return out;
}
