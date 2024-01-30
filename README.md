# openai-cli
Command line (CLI) application of OpenAI python client library

[MIT open source License](LICENSE).

## Setup

1. Create a virtual environment and activate it (this part can be skipped):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Copy the .env.example as .env and set OpenAi API Key. You can get one from here https://platform.openai.com/api-keys.
    ```bash
    cp .env.example .env
    ```

## Usage
openai_asst.py and openai_cli.py both provides comprehensive command line help messages to get you going.
Just run
```bash
./openai_asst.py --help
Usage: openai_asst.py [OPTIONS] COMMAND [ARGS]...
  Create and manage OpenAI assistant along with files from command line

Commands:
  checkfile  Check file paths and their size
  create     Create an assistant in OpenAI platform
  file       Create files in OpenAI platform to use with assistants
  info       Get detailed information about a particular assistant
  list       List assistants linked with OpenAI platform account
   ```
1. Create an OpenAI Assistant
```bash
./openai_asst.py create --help
Usage: openai_asst.py create [OPTIONS] NAME

Options:
  -m, --model TEXT  [default: gpt-3.5-turbo]
  -f, --files PATH  Maximum 2 files expected
  --file_ids TEXT   Provide comma separated id of files previously uploaded to OpenAI platform
  --help            Show this message and exit.
```

```bash
./openai_asst.py create myasst \
    -f ~/tmp/asst-training-file1.csv \
    -f ~/tmp/asst-training-file2.csv \
    --file_ids file-uploaded-before-id1,file-uploaded-before-id2
```

## Make conversation with the assistant
Set the newly created assistant id in .env file or provide it as option during conversation.
````
ASSISTANT_ID=asst_OPTMfmfxxxxXXXxxxZXyczDS
````
```bash
./openai_cli.py --help
Usage: openai_cli.py [OPTIONS] COMMAND [ARGS]...
  Make conversation with OpenAI models directly from command line

Commands:
  chat  Make conversations using OpenAI
  list  List messages in current or given thread
```
Start a new conversation with the assistant.
```bash
./openai_cli.py chat --new "who are you?"
```
Continue the conversation.
```bash
./openai_cli.py chat "what are your capabilities?"
```
