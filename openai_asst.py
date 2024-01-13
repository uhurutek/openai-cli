#!/usr/bin/env python3

"""
openai_asst.py

Create OpenAI assistant and get details of it.
Get list of assistants linked to an OpenAI platform account identified by OPENAI_API_KEY.

Author: Imtiaz Rahi <imtiaz.rahi@gmail.com>
Created on: 2024-01-10

Copyright (c) 2024 UhuruTek Solutions
License: MIT
"""
import importlib
import os

import click
import dotenv
from openai import OpenAI

from openai_utils import (show_json, bytes_to_human_readable,
                          str_to_bool, epoch_to_localtime)

GPT_ENV = 'openai.env'
# Sequence matters. GPT_ENV must be loaded first
dotenv.load_dotenv(GPT_ENV)
dotenv.load_dotenv()
chatgpt = OpenAI()
is_debug = str_to_bool(os.environ.get('DEBUG', default=False))
__version__ = importlib.metadata.version("openai-cli")


@click.group(help='Create and manage OpenAI assistant along with files from command line')
@click.version_option(__version__)
def asst():
    """openai_cli command entry point"""


@asst.command()
@click.argument('name')
@click.option('--model', '-m', default='gpt-3.5-turbo', show_default=True)
@click.option('--files', '-f', required=False, multiple=True,
              type=click.Path(exists=True), help='Maximum 2 files expected')
@click.option('--file_ids', required=False, type=str,
              help='Provide comma separated id of files previously uploaded to OpenAI platform')
def create(**kwargs):
    """Create an assistant in OpenAI platform"""
    if is_debug:
        print(f"Instructions: {os.environ.get('ASST_INSTRUCTION')}")
    instruct = os.environ.get('ASST_INSTRUCTION').strip()
    if instruct is None or not instruct:
        print('Assistant instructions are missing. Set ASST_INSTRUCTION in .env file.')
        return None
    # Process file IDs given in argument
    file_ids = kwargs['file_ids']
    if file_ids is not None:
        file_ids = str(file_ids).strip().split(',')
    else:
        file_ids = []
    # Process files given in argument
    files = kwargs['files']
    if files:
        if len(files) > 2:
            click.echo('Maximum 2 files can be provided', color=True)
            return False
        file_ids.extend(process_files(files))
    if is_debug:
        print(f'Going to create OpenAI assistant with these files: {file_ids}')

    asst_obj = chatgpt.beta.assistants.create(
        name=kwargs['name'],
        model=kwargs['model'],
        tools=asst_tools(),
        instructions=instruct,
        file_ids=file_ids
    )
    show_json(asst_obj)
    if is_debug:
        show_json(asst_obj)
    dotenv.set_key(GPT_ENV, "ASSISTANT_ID", asst_obj.id)
    return asst_obj.id


def process_files(file_objs) -> list[str]:
    """Upload files to OpenAI"""
    files = []
    for file_path in file_objs:
        try:
            with open(file_path, "rb") as each_file:
                res = chatgpt.files.create(file=each_file, purpose='assistants')
                files.append(res.id)
                if is_debug:
                    show_json(res)
                print(f'File: {res.id} was created of {bytes_to_human_readable(res.bytes)} bytes')
        except OSError as err:
            print(f"Error uploading file to OpenAI platform: {str(err)}")
    if is_debug:
        print(f'Files have been created in OpenAI platform {files}')
    return files


@asst.command(help='Create files in OpenAI platform to use with assistants')
# Can provide multiple file(s) separate by space. Max 20 file per assistant as per OpenAI rule
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def file(**kwargs) -> list[str]:
    """Create files in OpenAI platform to use with assistants"""
    files = kwargs['files']
    if not files:
        print('No files given')
        return []
    if len(files) > 20:
        click.echo('Maximum 20 files can be provided', color=True)
        return []

    return process_files(files)


def asst_tools():
    """Load assistant tools params from env and return them"""
    tools = []
    is_interpret = str_to_bool(os.environ.get('ASST_CODE_INTERPRETER', default=True))
    is_retrieval = str_to_bool(os.environ.get('ASST_RETRIEVAL', default=False))
    if is_interpret:
        tools.append({"type": "code_interpreter"})
    if is_retrieval:
        tools.append({"type": "retrieval"})
    return tools


@asst.command(help='Get detailed information about a particular assistant')
@click.argument('id', required=False, default=os.environ.get("ASSISTANT_ID"))
def info(**kwargs):
    """Get detailed information about a particular assistant"""
    asst_id = kwargs['id']
    if asst_id is None:
        print('Assistant id must be given as argument or in .env file')
        return
    bot = chatgpt.beta.assistants.retrieve(asst_id)
    if is_debug:
        show_json(bot)
    print_asst(bot)


def print_asst(bot):
    """Print assistant details in own format"""
    print(f"""  AsstId: {bot.id} | Created: {epoch_to_localtime(bot.created_at)}
  Name: {bot.name} \t\t\t| Model: {bot.model}
  Files: {bot.file_ids}
  Tools: {bot.tools}
  Instructions: {bot.instructions}""")


@asst.command(name='list', help='List assistants linked with OpenAI platform account')
def alist():
    """List assistants linked with the OpenAI platform account"""
    res = chatgpt.beta.assistants.list(order="desc", limit=20)
    if is_debug:
        show_json(res)
    for _, row in enumerate(res.data):
        print_asst(row)
        print('------------------------------------------------------------')


@asst.command(name='checkfile', help='Check file paths and their size')
# Provide file(s) separate by space
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def check_file(**kwargs):
    """Check file paths and their size"""
    for file_path in kwargs['files']:
        size = bytes_to_human_readable(os.path.getsize(file_path))
        print(f"Size of {file_path} is {size}")


if __name__ == '__main__':
    asst()
