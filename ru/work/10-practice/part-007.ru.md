## 10.7 Кодирование и декодирование Base58

Base58 — это алгоритм кодирования, который использует только определённые символы из таблицы Base64, исключая символы, выделенные в оригинале красным цветом. Первоначально он применялся для представления адресов биткойн-кошельков и был изобретён Сатоси Накамото.

**Таблица 10.2: Символы кодировки Base64**

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

Чтобы избежать неоднозначных символов, Base58 удаляет из таблицы Base64 символы 0 (ноль), O (заглавная буква O), I (заглавная буква i), l (строчная буква L), знак плюс (+) и косую черту (/). Оставшиеся 58 символов используются в качестве символов кодирования. Эти символы легко различимы и также предотвращают проблемы с переносами строк при копировании кода. Кодирование Base58 по сути представляет собой преобразование из одной системы счисления с большим основанием в другую. Сначала символ преобразуется в ASCII, а затем в десятичное число, после чего выполняется преобразование в систему счисления с основанием 58. Наконец, из таблицы кодирования выбирается соответствующий символ, формирующий строку в кодировке Base58. Однако из-за необходимости преобразования оснований эффективность кодирования Base58 относительно невысока. Алгоритм кодирования (10.1) иллюстрирует принцип кодирования.

Алгоритм 10.1: Алгоритм кодирования Base58 Данные: Исходная строка s

Результат: Закодированная строка b58_str

1 Инициализировать пустую строку b58_str для хранения результата. 2 for c ∈s do Преобразовать байт c в строке s в значение ASCII (основание 256). 3 Преобразовать число с основанием 256 в десятичное. 4 Преобразовать десятичное число в число с основанием 58. 5 Преобразовать число с основанием 58 в соответствующий символ согласно таблице символов Base58 6 Добавить полученный символ в b58_str. 7 8 end 9 Вернуть закодированную строку b58_str.

Декодирование — это процесс, обратный кодированию, и он также включает преобразование чисел между системами счисления с большим основанием. Символы строки Base58 сначала преобразуются в значения ASCII, затем в десятичные значения (основание 10), после чего — в значения с основанием 256, и, наконец, в символы ASCII. Процесс декодирования подробно описан в алгоритме (10.2).

Алгоритм 10.2: Алгоритм декодирования Base58 Данные: Закодированная строка b58

Результат: Декодированная строка new_str

1 Инициализировать пустую строку new_str для хранения результата 2 for c ∈b58 do Преобразовать байт c в строке b58 в значение ASCII (основание 58) 3 Преобразовать число с основанием 58 в десятичное значение (основание 10) 4 Преобразовать десятичное значение (основание 10) в значение с основанием 256 5 Преобразовать значение с основанием 256 в соответствующий символ ASCII 6 Добавить полученный символ в new_str 7 8 end 9 Вернуть декодированную строку new_str

Кодирование и декодирование по сути представляют собой двунаправленные преобразования строк между различными пространствами, аналогичные отображению в пространстве кодирования. Чтобы реализовать кодировщик и декодировщик Base58, сначала подготовим символы кодирования ALPHABET и таблицу преобразования кодов DIGITS_MAP. Кроме того, определим в качестве констант максимальное основание преобразования 58 и замену ведущего 0 символом 1. Использование констант в операциях предпочтительнее прямого использования «магических чисел», поскольку это улучшает читаемость кода.

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

Для обработки возможных ошибок во время кодирования и декодирования мы реализовали пользовательский тип ошибки для кодирования Base58, который позволяет обрабатывать недопустимые символы, ошибки длины и другие случаи. Для кодирования и декодирования были созданы два трейта — Encoder и Decoder соответственно. Encoder и Decoder содержат методы encode_to_base58 и decode_from_base58 соответственно.

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

На следующем шаге мы реализуем методы, соответствующие двум упомянутым выше трейтам. Хотя эти трейты реализуются для строк, для внутренних вычислений лучше использовать тип u8, поскольку символы в строке могут содержать несколько значений u8.

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

Декодирование — это процесс преобразования данных, закодированных в Base58, обратно в исходную форму, что по сути является преобразованием между системами счисления. Конкретная реализация метода декодирования выглядит следующим образом:

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

Ниже приведены результаты после кодирования и декодирования Base58.

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

С завершением реализации всего алгоритма Base58 аналогичными методами можно реализовать алгоритмы кодирования и декодирования для других интересующих схем кодирования, таких как Base32, Base36, Base62, Base64, Base85, Base92 и так далее. В главе 1 мы использовали Base64 для создания генератора паролей, но его также можно заменить на Base58. Я уже выполнил такую замену и включил соответствующий код в репозиторий, относящийся к данной главе.
