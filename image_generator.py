import os
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types

IMAGE_TOOLS = {
    "open_an_image": {
        "name": "open_an_image",
        "description": "Open and read an image file, returning the binary data.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The file path to the image."}
            },
            "required": ["path"]
        }
    },
    "move_the_image": {
        "name": "move_the_image",
        "description": "Move an image file from one location to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "path_before": {"type": "string", "description": "The current file path of the image."},
                "path_after": {"type": "string", "description": "The new file path where the image should be moved."}
            },
            "required": ["path_before", "path_after"]
        }
    },
    "generate_image": {
        "name": "generate_image",
        "description": "Generate an image from a text prompt using the Gemini API.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The text prompt to generate the image from."},
                "dimensions": {"type": "string", "description": "The desired dimensions for the generated image (e.g., '512x512')."},
                "path": {"type": "string", "description": "The directory path to save the image. If None or empty, saves to the current working directory."},
                "name_of_image": {"type": "string", "description": "The name to use for the saved image file (without extension)."}
            },
            "required": ["prompt", "dimensions", "path", "name_of_image"]
        }
    },
    "modify_image": {
        "name": "modify_image",
        "description": "Modify an existing image based on a text prompt using the Gemini API.",
        "parameters": {
            "type": "object",
            "properties": {
                "path_of_the_image_to_modify": {"type": "string", "description": "Path to the image file to be modified."},
                "path_to_save_the_image": {"type": "string", "description": "Directory path to save the modified image. If None or empty, saves to the current working directory."},
                "prompt": {"type": "string", "description": "The text prompt describing the modification to apply."},
                "name_of_image": {"type": "string", "description": "The name to use for the saved modified image file (without extension)."},
                "dimensional_preference": {"type": "string", "description": "Additional dimensional preferences for the modification (e.g., '512x512')."}
            },
            "required": ["path_of_the_image_to_modify", "path_to_save_the_image", "prompt", "name_of_image", "dimensional_preference"]
        }
    }
}


def open_an_image(path):

    """Open and read an image file.

    Args:
        path (str): The file path to the image.

    Returns:
        bytes: The binary data of the image.

    Raises:
        FileNotFoundError: If the image file does not exist at the given path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")

    with open(path, 'rb') as f:
        image_data = f.read()

    return image_data


def move_the_image(path_before, path_after):

    """Move an image file from one location to another.

    Args:
        path_before (str): The current file path of the image.
        path_after (str): The new file path where the image should be moved.

    Raises:
        FileNotFoundError: If the image file does not exist at the current path.
        OSError: If the destination directory does not exist and cannot be created.
    """

    if not os.path.exists(path_before):
        raise FileNotFoundError(f"The file at {path_before} does not exist.")

    if not os.path.exists(os.path.dirname(path_after)):
        os.makedirs(os.path.dirname(path_after), exist_ok=True)

    os.rename(path_before, path_after)
    print(f"Image moved from {path_before} to {path_after}")

def generate_image(prompt, dimensions, path, name_of_image):

    """Generate an image from a text prompt using the Gemini API.

    Args:
        prompt (str): The text prompt to generate the image from.
        dimensions (str): The desired dimensions for the generated image (not currently used in the function, but can be used for future extension).
        path (str): The directory path to save the image. If None or empty, saves to the current working directory.
        name_of_image (str): The name to use for the saved image file (without extension).

    Returns:
        None

    Raises:
        Exception: If there is an error with the API request or image saving.
    """

    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt+dimensions,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:

        if part.text is not None:
            print(part.text)

        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))

    if not path:
        save_path = os.path.join(os.getcwd(), f"{name_of_image}.png")

    else:
        os.makedirs(path, exist_ok=True)
        save_path = os.path.join(path, f"{name_of_image}.png")

    image.save(save_path)
    print(f"Image {name_of_image} saved to {save_path}")


def modify_image(path_of_the_image_to_modify, path_to_save_the_image, prompt, name_of_image, dimensional_preference):
    """Modify an existing image based on a text prompt using the Gemini API.

    Args:
        path_of_the_image_to_modify (str): Path to the image file to be modified.
        path_to_save_the_image (str): Directory path to save the modified image. If None or empty, saves to the current working directory.
        prompt (str): The text prompt describing the modification to apply.
        name_of_image (str): The name to use for the saved modified image file (without extension).
        dimensional_preference (str): Additional dimensional preferences for the modification (e.g., '512x512').

    Returns:
        None

    Raises:
        Exception: If there is an error with the API request, image processing, or image saving.
    """
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(

        model="gemini-2.0-flash-preview-image-generation",
        contents=[prompt+dimensional_preference, path_of_the_image_to_modify],
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)

        elif part.inline_data is not None:

            image = Image.open(BytesIO(part.inline_data.data))

            if not path_to_save_the_image:
                save_path = os.path.join(os.getcwd(), f"{name_of_image}.png")

            else:
                os.makedirs(path_to_save_the_image, exist_ok=True)
                save_path = os.path.join(path_to_save_the_image, f"{name_of_image}.png")

            image.save(path_to_save_the_image)
            print(f"Image {name_of_image} saved to {path_to_save_the_image}")
import os
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types

def open_an_image(path):
    """Open and read an image file.

    Args:
        path (str): The file path to the image.

    Returns:
        bytes: The binary data of the image.

    Raises:
        FileNotFoundError: If the image file does not exist at the given path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")

    with open(path, 'rb') as f:
        image_data = f.read()

    return image_data

def move_the_image(path_before, path_after):
    """Move an image file from one location to another.

    Args:
        path_before (str): The current file path of the image.
        path_after (str): The new file path where the image should be moved.

    Raises:
        FileNotFoundError: If the image file does not exist at the current path.
        OSError: If the destination directory does not exist and cannot be created.
    """
    if not os.path.exists(path_before):
        raise FileNotFoundError(f"The file at {path_before} does not exist.")

    if not os.path.exists(os.path.dirname(path_after)):
        os.makedirs(os.path.dirname(path_after), exist_ok=True)

    os.rename(path_before, path_after)
    print(f"Image moved from {path_before} to {path_after}")

def generate_image(prompt, dimensions, path, name_of_image):
    """Generate an image from a text prompt using the Gemini API.

    Args:
        prompt (str): The text prompt to generate the image from.
        dimensions (str): The desired dimensions for the generated image (not currently used in the function, but can be used for future extension).
        path (str): The directory path to save the image. If None or empty, saves to the current working directory.
        name_of_image (str): The name to use for the saved image file (without extension).

    Returns:
        None

    Raises:
        Exception: If there is an error with the API request or image saving.
    """
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt+dimensions,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))

    if not path:
        save_path = os.path.join(os.getcwd(), f"{name_of_image}.png")
    else:
        os.makedirs(path, exist_ok=True)
        save_path = os.path.join(path, f"{name_of_image}.png")

    image.save(save_path)
    print(f"Image {name_of_image} saved to {save_path}")

def modify_image(path_of_the_image_to_modify, path_to_save_the_image, prompt, name_of_image, dimensional_preference):
    """Modify an existing image based on a text prompt using the Gemini API.

    Args:
        path_of_the_image_to_modify (str): Path to the image file to be modified.
        path_to_save_the_image (str): Directory path to save the modified image. If None or empty, saves to the current working directory.
        prompt (str): The text prompt describing the modification to apply.
        name_of_image (str): The name to use for the saved modified image file (without extension).
        dimensional_preference (str): Additional dimensional preferences for the modification (e.g., '512x512').

    Returns:
        None

    Raises:
        Exception: If there is an error with the API request, image processing, or image saving.
    """
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=[prompt+dimensional_preference, path_of_the_image_to_modify],
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))

            if not path_to_save_the_image:
                save_path = os.path.join(os.getcwd(), f"{name_of_image}.png")
            else:
                os.makedirs(path_to_save_the_image, exist_ok=True)
                save_path = os.path.join(path_to_save_the_image, f"{name_of_image}.png")

            image.save(save_path)
            print(f"Image {name_of_image} saved to {save_path}")
