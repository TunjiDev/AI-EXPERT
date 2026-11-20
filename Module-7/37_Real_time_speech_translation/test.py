import asyncio
from googletrans import Translator

async def test_translation():
    try:
        async with Translator() as translator:
            result = await translator.translate(
                "Hello, how are you?",
                dest="es",
                src="en"
            )

            print("Original:", "Hello, how are you?")
            print("Translated:", result.text)

    except Exception as error:
        print("Something went wrong:", repr(error))

asyncio.run(test_translation())