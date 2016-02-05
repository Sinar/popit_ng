from django:python2

# Just make sure pip latest version so it does not complain
RUN pip install --upgrade pip 

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

# Copy all code over for production deployment
# Dev will use override to VOLUME mount local code 
COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

# Any other extra software; put it here ...
# Below are some standard sysadmin tools I use
# Might want to add so can use ps auxwwf and less
RUN apt-get update && apt-get install -y \
		vim \
		htop \
		sysstat \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

EXPOSE 8000 

VOLUME "/usr/src/app"


