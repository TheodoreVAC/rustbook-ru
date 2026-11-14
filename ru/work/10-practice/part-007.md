## 10.7 Base58 Encode and Decode

Base58 is an encoding algorithm that only uses certain characters from the Base64 table, removing the characters highlighted in red. It was originally used to represent Bitcoin wallet addresses and was invented by Satoshi Nakamoto.

**Table 10.2: Base 64 encoding characters**

| ASCII | Char | ASCII | Char | ASCII | Char | ASCII | Char | ASCII | Char |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 13 | D | 26 | Q | 39 | d | 52 | q |
| 1 | 1 | 14 | E | 27 | R | 40 | e | 53 | r |
| 2 | 2 | 15 | F | 28 | S | 41 | f | 54 | s |
| 3 | 3 | 16 | G | 29 | T | 42 | g | 55 | t |
| 4 | 4 | 17 | H | 30 | U | 43 | h | 56 | u |
| 5 | 5 | 18 | I | 31 | V | 44 | i | 57 | v |
| 6 | 6 | 19 | J | 32 | W | 45 | j | 58 | w |
| 7 | 7 | 20 | K | 33 | X | 46 | k | 59 | x |
| 8 | 8 | 21 | L | 34 | Y | 47 | l | 60 | y |
| 9 | 9 | 22 | M | 35 | Z | 48 | m | 61 | z |
| 10 | A | 23 | N | 36 | a | 49 | n | 62 | + |
| 11 | B | 24 | O | 37 | b | 50 | o | 63 | / |
| 12 | C | 25 | P | 38 | c | 51 | p |  |  |

To avoid ambiguous characters, Base58 removes 0 (zero), O (capital O), I (capital i), l (lowercase L), plus sign (+), and slash (/) from the Base64 table. The remaining 58 characters are used as encoding characters. These characters are easily distinguishable and also prevent problems with line breaks when copying the code. Base58 encoding is essentially a conversion from a large number base. First, the character is converted to ASCII and then to decimal, followed by 58 base conversion. Finally, the corresponding character is selected from the encoding table to form the Base58 encoding string. However, due to the need for base conversion, the efficiency of Base58 encoding is relatively low. The encoding algorithm (10.1) illustrates the encoding principle.

Algorithm 10.1: Base58 Encoding Algorithm Data: Original string s

Result: Encoded string b58_str

1 Initialize an empty string b58_str to store the result. 2 for c ∈s do Convert byte c in s to ASCII value (256 base). 3 Convert 256 base number to decimal. 4 Convert decimal number to 58 base number. 5 Convert 58 base number to corresponding character according to the Base58 character 6 table. Append the resulting character to b58_str. 7 8 end 9 Return the encoded string b58_str.

Decoding is the reverse process of encoding and involves converting from a large number base. The characters in the Base58 string are first converted to ASCII values, then to 10 decimal values, followed by conversion to 256 decimal values, and finally to ASCII characters. The decoding process is described in detail in Algorithm (10.2).

Algorithm 10.2: Base58 Decoding Algorithm Data: Encoded string b58

Result: Decoded string new_str

1 Initialize an empty string new_str to store the result 2 for c ∈b58 do Convert byte c in b58 to ASCII value (58 base) 3 Convert 58 base number to 10 decimal value 4 Convert 10 decimal value to 256 decimal value 5 Convert 256 decimal value to corresponding ASCII character 6 Append the resulting character to new_str 7 8 end 9 Return the decoded string new_str

Encoding and decoding are essentially two-way string transformations between different spaces, similar to a mapping in the encoding space. To implement a Base58 encoder and decoder, we first prepare the encoding characters ALPHABET and the encoding conversion table DIGITS_MAP. Additionally, we define the maximum conversion base 58 and substitute 1 for the leading 0 as constants. Using constants for operations is preferable to using magic numbers directly, as it improves code readability.

```text
// base58.rs

// Conversion base 58
const BIG_RADIX: u32 = 58;

// Substitute 1 for the leading 0
const ALPHABET_INDEX_0: char = '1';

// Base58 encoding characters
const ALPHABET: &[u8;58] = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZ
abcdefghijkmnopqrstuvwxyz";

// Mapping relationship between the bases
const DIGITS_MAP: &'static [u8] = &[
  255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
  255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
  255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
  255, 0, 1, 2, 3, 4, 5, 6, 7,
     8,255,255,255,255,255,255, 255, 9, 10, 11, 12, 13, 14, 15, 16,255, 17, 18, 19, 20,
     21,255, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
      32,255,255,255,255,255, 255, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,255, 44, 45,
     46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
      57,255,255,255,255,255, ];
```

To handle potential errors during encoding and decoding, we have implemented a custom error type for Base58 encoding to manage illegal characters, length errors, and other cases. Two traits, Encoder and Decoder, have been created for encoding and decoding, respectively. Encoder and Decoder contain the methods encode_to_base58 and decode_from_base58, respectively.

```rust
// base58.rs

// Decoding error type
#[derive(Debug, PartialEq)]
pub enum DecodeError {
    Invalid,
    InvalidLength,
    InvalidCharacter(char, usize),
}

// Encoding and decoding traits
pub trait Encoder {
    // Encoding method
    fn encode_to_base58(&self) -> String;
}

pub trait Decoder {
    // Decoding method
    fn decode_from_base58(&self) ->Result<String,DecodeError>;
}
```

In the next step, we will implement the methods that correspond to the two traits mentioned earlier. Although these traits are implemented for strings, it is better to use u8 for internal calculations since the characters in the string may contain multiple u8 values.

```rust
// base58.rs

// Implement Base58 encoding
impl Encoder for str {
    fn encode_to_base58(&self) -> String {
        // Convert to bytes for processing
        let str_u8 = self.as_bytes();
        // Count the number of leading zeros
        let zero_count = str_u8.iter()
                               .take_while(|&&x| x == 0)
                               .count();
        // Space required after conversion is log(256)/log(58),
        // which is approximately 1.38 times the original data.
        // We don't need leading zeros
        let size = (str_u8.len() - zero_count) * 138 / 100 + 1;
        // Convert characters from one base to another
        let mut i = zero_count;
        let mut high = size - 1;
        let mut buffer = vec![0u8; size];
        while i < str_u8.len() {
            // j is the decreasing index, corresponding to
            // counting from the back
            let mut j = size - 1;
```

```rust
            // carry is the character read from the front
            let mut carry = str_u8[i] as u32;

            // Store the converted data from back to front
            // in turn
            while j > high || carry != 0 {
                carry += 256 * buffer[j] as u32;
                buffer[j] = (carry % BIG_RADIX) as u8;
                carry /= BIG_RADIX;

                if j > 0 {
                    j -= 1;
                }
            }
            i += 1;
            high = j;
        }

        // Handle multiple leading zeros
        let mut b58_str = String::new();
        for _ in 0..zero_count {
            b58_str.push(ALPHABET_INDEX_0);
        }

        // Get the encoded characters and concatenate
        // them into a string
        let mut j = buffer.iter()
                          .take_while(|&&x| x == 0)
                          .count();
        while j < size {
            b58_str.push(ALPHABET[buffer[j] as usize] as char);
            j += 1;
        }

        // Return the encoded string
        b58_str
    }
}
```

Decoding is the process of converting Base58 encoded data back to its original form, which is essentially a conversion between numeral systems. The specific implementation of the decoding method is as follows:

```rust
// base58.rs

// Implement Base58 decoding
impl Decoder for str {
    fn decode_from_base58(&self) -> Result<String,DecodeError>
{
        // Store conversion characters
        let mut bin = [0u8; 132];
        let mut out = [0u32; (132 + 3) / 4];
```

```rust
        // Number of remaining bits after processing data
        // in units of 4
        let bytes_left = (bin.len() % 4) as u8;
        let zero_mask = match bytes_left {
            0 => 0u32,
            _ => 0xffffffff << (bytes_left * 8),
        };

        // Count leading zeros
        let zero_count = self.chars()
                        .take_while(|&x| x == ALPHABET_INDEX_0)
                        .count();

        let mut i = zero_count;
        let b58: Vec<u8> = self.bytes().collect();
        while i < self.len() {
            // Invalid characters
            if (b58[i] & 0x80) != 0 {
                return Err(DecodeError::InvalidCharacter(
                            b58[i] as char, i));
            }
            if DIGITS_MAP[b58[i] as usize] == 255 {
                return Err(DecodeError::InvalidCharacter(
                            b58[i] as char, i));
            }

            // Number system conversion
            let mut j = out.len();
            let mut c = DIGITS_MAP[b58[i] as usize] as u64;
            while j != 0 {
                j -= 1;
                let t = out[j] as u64 * (BIG_RADIX as u64) + c;
                c = (t & 0x3f00000000) >> 32;
                out[j] = (t & 0xffffffff) as u32;
            }

            // Data is too long
            if c != 0 {
                return Err(DecodeError::InvalidLength);
            }

            if (out[0] & zero_mask) != 0 {
                return Err(DecodeError::InvalidLength);
            }

            i += 1;
        }

        // Handle remaining bits
        let mut i = 1;
        let mut j = 0;
```

```rust
        bin[0] = match bytes_left {
            3 => ((out[0] & 0xff0000) >> 16) as u8,
            2 => ((out[0] & 0xff00) >> 8) as u8,
            1 => {
                j = 1;
                (out[0] & 0xff) as u8
            },
            _ => {
                i = 0;
                bin[0]
            }
        };

        // Process data in units of 4 and
        // use bit shifting for division
        while j < out.len() {
            bin[i] = ((out[j] >> 0x18) & 0xff) as u8;
            bin[i + 1] = ((out[j] >> 0x10) & 0xff) as u8;
            bin[i + 2] = ((out[j] >> 8) & 0xff) as u8;
            bin[i + 3] = ((out[j] >> 0) & 0xff) as u8;
            i += 4;
            j += 1;
        }

        // Get number of leading zeros
        let leading_zeros = bin.iter()
                               .take_while(|&&x| x == 0)
                               .count();

        // Get decoded string
        let new_str = String::from_utf8(
                        bin[leading_zeros - zero_count..]
                        .to_vec());

        // Return valid result
        match new_str {
            Ok(res) => Ok(res),
            Err(_) => Err(DecodeError::Invalid),
        }
    }
}

fn main() {
    println!("{:#?}","abc".encode_to_base58());
    println!("{:#?}","ZiCa".decode_from_base58().unwrap());

    println!("{:#?}","loverust".encode_to_base58());
    println!("{:#?}","K8xdoM2VJtK".decode_from_base58());

    println!("{:#?}","iloveyou".encode_to_base58());
    println!("{:#?}","Jdjxs3pmuK2".decode_from_base58());
}
```

The following are the results after Base58 encoding and decoding.

```text
"ZiCa"
"abc"
"K8xdoM2VJtK"
Ok(
    "loverust",
)
"Jdjxs3pmuK2"
Ok(
    "iloveyou",
)
```

With the completion of the entire Base58 algorithm, similar methods can be used to implement encoding and decoding algorithms for other encoding schemes of interest, such as Base32, Base36, Base62, Base64, Base85, Base92, and so on. In Chapter 1, we used Base64 to create a password generator, but it can also be replaced with Base58. I have already made the replacement and included the specific code in the corresponding repository for this chapter.
