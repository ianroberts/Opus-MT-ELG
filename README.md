# Opus-MT ELG API

This is a simple extension of the standard [Opus-MT](https://github.com/Helsinki-NLP/Opus-MT) server Docker container to make the API compatible with the requirements of the European Language Grid.

## Building

First build the base Docker image from a completely clean clone of the master branch of https://github.com/Helsinki-NLP/Opus-MT:

```
cd ..../Opus-MT
docker build -t opus-mt .
```

Now in this folder, download the models

```
./fetch-models.sh
```

and finally build the ELG Docker image with

```
docker build -t opus-mt-elg .
```
