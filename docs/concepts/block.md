# Blocks

INTELMO divides an article into a group of blocks. Developers can perform operations on these blocks and then return a new group of blocks.

## What is a block?

A block could be a paragraph, a sentence or a word. It is a basic unit of an article. When INTELMO fetches an article from RSS feeds, it will divide the article into a group of blocks, each of which is a paragraph by default. A block has the following fields:

- `level`: The level of the block, which could be `paragraph`, `sentence` or `word`. The rendering of a paragraph includes inter-paragraph spacing. INTELMO also provides a `global` level, which is shown on the top of the reader.

- `type`: Different types of blocks have different styles. For example, a block with type `bold` will be rendered in bold.

- `content`: the content of the block, which is a string.

- `children`: a list of blocks. If a block has children, it will be rendered as a container. Otherwise, it will be rendered as a leaf. Details are shown in the [Nesting blocks](#nesting-blocks) section.

```python
Block(
    level="paragraph",
    type="bold",
    content="Some paragraph content",
    children=[]
)
```

## Nesting blocks

As shown above, each block has a `children` field, which is a list of blocks or set to empty by default. Developers can nest blocks by setting the `children` field. When INTELMO recieves a block with children, it will render the children blocks inside the block itself. Otherwise, it will render the parent block with it's own content and style.

```python
Block(
    level="paragraph",
    type="bold", # type omitted when children is not empty
    content="", # content omitted when children is not empty
    children=[
        Block(
            level="sentence",
            type="italic",
            content="Here is one sentence.",
            children=[] # children can be empty
        ),

        Block(
            level="sentence",
            type="italic", # type omitted when children is not empty
            content="", # content omitted when children is not empty
            children=[
                Block(
                    level="word",
                    type="underline",
                    content="happy",
                    children=[]
                ),
                Block(
                    level="word",
                    type="normal",
                    content="dog.",
                    children=[]
                )
            ]
        )
    ]
)
```

<div class="w-full px-9 py-6 border rounded">
<span class="font-italic">Here is one sentence.</span> <span class="underline">happy</span> <span class="">dog.</span>
</div>

## Available Configurations

### Block Level

The `level` field of a block can be set to `paragraph`, `sentence`, `word` or `global`.

<div class="w-full py-9 px-6 border relative rounded">
  
  <div class="w-full p-1 border border-blue-500 relative">
    <div class="absolute top-0 -mt-6 -ml-1 rounded-t bg-blue-500 px-1">
      <label class="text-white text-xs">paragraph</label>
    </div>
    In a groundbreaking discovery, scientists aboard the research vessel <span class="border-purple-500 border rounded">"Aquatica"</span><span class="text-white text-xs bg-purple-500 px-1 rounded-r">word</span> have reportedly uncovered a new species of bioluminescent jellyfish in the uncharted depths of the Mariana Trench. <span class="underline decoration-sky-500">The newly dubbed "Luminaris abyssus" emits an ethereal blue and green glow, illuminating its surroundings in a mesmerizing dance of light.
    <span class="text-white text-xs bg-sky-500 px-1 rounded">sentence</span>
    </span>
  </div>
</div>

### Block Type

<!-- class BlockTypeEnum(Enum):
    """Enum for type of block"""
    Normal = "normal"
    Bold = "bold"
    Italic = "italic"
    Underline = "underline"
    Light = "light"
    Title = "title"
    Custom = "custom"
    Quote = "quote" -->

<!-- a table of two columns, left column is type, right column is a div -->

| Type        | Example                                                                                                                                |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| "normal"    | <div class="p-1 bg-white text-black border rounded">The quick brown fox jumps over the lazy dog.</div>                                 |
| "bold"      | <div class="font-bold p-1 bg-white text-black border rounded">The quick brown fox jumps over the lazy dog.</div>                       |
| "italic"    | <div class="italic p-1 bg-white text-black border rounded">The quick brown fox jumps over the lazy dog.</div>                          |
| "underline" | <div class="underline p-1 bg-white text-black border rounded">The quick brown fox jumps over the lazy dog.</div>                       |
| "light"     | <div class="text-gray-400 p-1 bg-white border rounded">The quick brown fox jumps over the lazy dog.</div>                              |
| "title"     | <div class="text-xl p-1 bg-white text-black border rounded font-semibold capitalize">The quick brown fox jumps over the lazy dog</div> |
| "quote"     | <div class="border-blue-500 border bg-blue-200 text-blue-800 underline p-1 rounded">The quick brown fox jumps over the lazy dog.</div> |
