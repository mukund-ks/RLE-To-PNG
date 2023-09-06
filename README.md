## RLE to PNG

A utility script to convert Run-Length-Encoded Binary Masks in Darwin JSON 2.0 from [V7 Labs](https://www.v7labs.com/) to PNG.

The script must receive a JSON document that complies with the Darwin JSON 2.0 Format. [Refer here](https://docs.v7labs.com/reference/darwin-json).

## Example

Binary Mask annotated in JSON. [See here](Data/Image_2.json).


| <img src="Mask/Image_2_mask.png" alt="drawing" width="500"/> |
| :----------------------------------------------------------: |
|                 *Binary Mask in PNG Format*                  |

## Installation

1. Clone the Repository
   ```console
   git clone https://github.com/mukund-ks/RLE-To-PNG.git
   ```

2. Move into your local copy of repo
   ```console
   cd RLE-to-PNG
   ```

3. Setup a Virtual Environment
   ```console
   python -m venv env
   ```

4. Activate the Virtual Environment
   ```console
   env/Scripts/activate
   ```

5. Install Dependencies
   ```console
   pip install -r requirements.txt
   ```

## Usage

* Run the 'help' command to see accepted arguments.
```console
python main.py --help
```

```console
Usage: main.py [OPTIONS]

  Utility script to convert Darwin 2.0 JSON Binary Masks from V7Labs to PNG. The masks should be 
  Run-Length-Encoded and the JSON document should be following the Darwin 2.0 JSON Format.

  Args:     
    mask_dir (str): Mask Directory with Darwin 2.0 JSON files.

  Raises:     
    OSError: In the event that provided directory does not exist.

Options:
  -M, --mask-dir TEXT  Directory with Masks as JSON files  [required]
  --help               Show this message and exit.
```

* An example
```console
python main.py --mask-dir Data
```
