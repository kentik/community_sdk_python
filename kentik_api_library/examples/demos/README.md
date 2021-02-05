# Running jupyter-notebook demos

Precondition: python3 and pip3 are already installed.

1. Install virtualenv - this allows you to create a python sandbox for your project  
`pip3 install virtualenv`

1. Create new virtual environment   
`virtualenv .venv`

1. Activate virtualenv  
`source .venv/bin/activate`

1. Clone the library repo  
`git clone https://github.com/kentik/community_sdk_python.git`

1. `cd community_sdk_python/`

1. Install the library from repo  
`pip install -e kentik_api_library/`

1. Install demo requirements  
`pip3 install Pillow pandas httpretty`

1. Install jupyter-notebook  
`pip3 install notebook`

1. Run throttling demo  
`jupyter-notebook kentik_api_library/examples/demos/throttling_retry_demo.ipynb`
