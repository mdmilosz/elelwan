# elelwan

**elelwan** is an idea of a constructed language parseable with an LL(1) parser (hence the name).

It depends on:
* **LLgen**, which can be found on [SlackBuilds.org](https://slackbuilds.org/repository/13.37/development/LLgen/),
* **flex**,
* **gcc**,
* **Python 3.5**,
* **GNU make**.

It builds upon two files: `dict.txt` (the dictionary) and `gram.txt` (the grammar). The result is an executable written to the file `out`.

You can build it by typing `make`, or try a sample input by typing `make test`.

The filenames can be overriden by environment variables `DICT`, `GRAM` and `OUT`. For example, the following command will build the executable using alternative dictionary and grammar files:

```
make DICT=alt-dict.txt GRAM=alt-gram.txt
```

(Before changing between different environments, you might want to `make clean`.)

## dict.txt

The dictionary consists of lines of the form: *word part-of-speech translation*, separated by whitespace, f.i.:

```
ala Noun Alice
ma Verb has
kota Noun a.cat
```

The part of speech symbol doubles as a token name.

In order to omit the translation, leave `-` (a single dash).

## gram.txt

The grammar consists of a header and a body, separated by `%%`.

The header consists of `%token` and `%start` declarations.
* `%token`, followed by one or more token names, declares them as part of speech names.
* `%start`, followed by one symbols, declares it as the starting symbol of the grammar.

**Update:** The `%token` declarations are now generated automatically. They shouldn't be included in the grammar file.

The body consists of lines of the form *parent-symbol = child-symbols*, where *child-symbols* is a list of symbols the parent can be decomposed into. Basic LLgen extensions are supported: `[ ] | + * ?`.

An example grammar looks as follows:

```
%start Sentence
%%
Sentence = NounPhrase VerbPhrase
NounPhrase = Noun
VerbPhrase = Verb Noun
```

## out

The output executable works as follows: for a given input, it decomposes it into words and then parses it according to the grammar, outputting a syntax tree in bracketed form.

For instance, for the input of `ala ma kota`, the aforementioned grammar should output:

```
[Sentence
  [NounPhrase
    [Noun ala  # Alice]
  ]
  [VerbPhrase
    [Verb ma  # has]
    [Noun kota  # a.cat]
  ]
]
```

(The output can be later converted into an image using e.g. Miles Shang's [syntree](http://mshang.ca/syntree/) or Yoichiro Hasebe's [RSyntaxTree](http://www.yohasebe.com/rsyntaxtree/).)
