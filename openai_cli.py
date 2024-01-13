#!/usr/bin/env python3

"""
openai_cli.py

OpenAI cli is a simple command line application to make conversations
with GPT models using OpenAI platform.

Start and continue chat conversation with a ChatGPT model.
Already configured OpenAI assistant must be provided to use this program.
Create OpenAI assistant using the openai_asst.py program and then provide ASSISTANT_ID in .env file.

This program uses the OpenAI python client.

NOTE:
OPENAI_API_KEY must be set to in .env file.
"Create new secret key" in API keys page https://platform.openai.com/account.

Author: Imtiaz Rahi <imtiaz.rahi@gmail.com>
Created on: 2024-01-10

Copyright (c) 2024 UhuruTek Solutions
License: MIT
"""
import importlib
import os
import shutil
import time
from pprint import pprint

import click
import dotenv
from openai import OpenAI

from openai_utils import show_json, datetime_str, str_to_bool

GPT_ENV = 'openai.env'
dotenv.load_dotenv(GPT_ENV)
dotenv.load_dotenv()
chatgpt = OpenAI()
# set DEBUG=True or DEBUG=1 in shell environment or .env file
is_debug = str_to_bool(os.environ.get('DEBUG', default=False))
__version__ = importlib.metadata.version("openai-cli")


@click.group(help='Make conversation with OpenAI models directly from command line')
@click.version_option(__version__)
def cli():
    """openai_cli command entry point"""


@cli.command(name='list', help='List messages in current or given thread')
@click.argument('thread_id', required=False)
def alist(**kwargs):
    """Return a simple list of the messages in conversation thread"""
    thread = kwargs['thread_id']
    if thread is None:
        thread = os.environ.get('GPT_THREAD')

    msg = chatgpt.beta.threads.messages.list(thread_id=thread, order='asc')
    # NOTE: Uncomment to view JSON output
    if is_debug:
        show_json(msg)

    print(f'Full conversation in {thread}')
    res = []
    for idx, row in enumerate(msg.data):
        val = row.content[0].text.value
        res.append(val)
        print(f'{idx + 1}: {val}')
    return res


@cli.command(help='Make conversations using OpenAI')
@click.argument('msg')
@click.option('--new', is_flag=True, default=False, help='Start a new conversation thread')
@click.option('--asst', default=os.environ.get("ASSISTANT_ID"), required=False,
              show_default=True, help='ChatGPT assistant id')
def chat(**kwargs):
    """Make conversation using OpenAI"""
    asst_id = kwargs['asst']
    if asst_id is None:
        print('One OpenAI assistant id must be given. Create one using openai_asst.py')
        return None

    if kwargs['new']:
        return new_chat(**kwargs)

    click.echo(message='Continuing chat conversation ', nl=False, color=True)
    return chat_response(os.environ.get('GPT_THREAD'), kwargs['msg'], asst_id)


def new_chat(**kwargs):
    """Create a new chat conversation thread in ChatGPT"""
    if os.path.exists(GPT_ENV):
        # Better keep backup copy of last GPT_ENV before starting a new thread
        # rather than rename it
        shutil.copy(GPT_ENV, f'{GPT_ENV}.{datetime_str()}')
    else:
        with open(GPT_ENV, 'w', encoding='utf-8') as file:
            file.close()

    # Create a new OpenAI thread
    thread = chatgpt.beta.threads.create()
    click.echo(message='New chat conversation ', nl=False, color=True)
    # Save the thread id to continue conversation
    dotenv.set_key(GPT_ENV, "GPT_THREAD", thread.id)
    # Let's keep track of the asst in our own GPT_ENV
    dotenv.set_key(GPT_ENV, "ASSISTANT_ID", kwargs['asst'])
    return chat_response(thread.id, kwargs['msg'], kwargs['asst'])


def chat_response(thread_id: str, msg: str, asst_id: str):
    """Get response for the message given as input
    1. create message in the thread
    2. create a run for the assistant in that thread
    3. run the thread and check steps for completion
    4. get only the response given by GPT
    """
    click.echo(message=f'with {thread_id}', color=True)
    # Add a Message to the Thread created
    msg = chatgpt.beta.threads.messages.create(thread_id=thread_id, role="user", content=msg)

    # Run the Assistant in that thread with message already inserted
    run = chatgpt.beta.threads.runs.create(thread_id=thread_id, assistant_id=asst_id)

    # Check the Run status for completion
    run = wait_on_run(thread=thread_id, run=run)

    # Retrieve and display the ChatGPT assistant response
    msgs = chatgpt.beta.threads.messages.list(thread_id=thread_id, order="asc", after=msg.id)
    if is_debug:
        show_json(msgs)
    rs = {'ques': msg.content[0].text.value, 'answ': msgs.data[0].content[0].text.value}
    pprint(rs)
    return rs


def wait_on_run(run, thread):
    """Check open thread run status till completed or cancelled"""
    while run.status in ('queued', 'in_progress'):
        run = chatgpt.beta.threads.runs.retrieve(thread_id=thread, run_id=run.id)
        time.sleep(int(os.environ.get('GPT_RUN_SLEEP', 3)))
    return run


if __name__ == '__main__':
    cli()
