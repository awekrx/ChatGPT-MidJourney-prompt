# ChatGPT-MidJourney-prompt

This is a ChatGPT based prompt generation model for MidJourney. The purpose of this model is to simplify the creation of images and increase their creativity. By introducing a partial hint, ChatGPT creates a follow-up that can be used to stimulate creativity and provide new ideas.

## What's new
>
> 24.03.2023

Create PyPi project. Update file structure, add api key authentication to ChatGPT.
__CLI-app and discord-bot will be available within a few days.__

## Installation

```bash
pip install chatGPTMidJourneyPrompt
```

## Usage

```py
   from chatGPTMidJourneyPrompt.mjPrompt import PromptGenerator

   # supported authorization methods: via email and password, via token, via api key
   config = {
      "email": "your_email",
      "password": "your_password",
      # or
      "session_token": "your_session_token",
      # or
      "api_key": "your_api_key",
   }

   promptGenerator = PromptGenerator(config)

   prompt = promptGenerator.V5("any text")
   prompt = promptGenerator.V4("any text")
   prompt = promptGenerator.niji("any text")
   prompt = promptGenerator.testp("any text")

   # or advanced usage if needed
   promptConfig = {
      model: "artistic"
      type: "anime",
      renderer: "ray tracing",
      content: "character",
      aspect_ratio: "1:5",
      color: "red",
      url: "example image url"
   }

   prompt = promptGenerator.V5("any text", config=promptConfig, words=50)
```

## More about config

### All config properties

|model|type|renderer|content|aspect_ratio|color|url|
|---|---|---|---|---|---|---|
|weights, artistic|anime, photorealistic, avatar, couple avatar|octane, unreal engine, ray tracing, mixed|character, landscape, object, light, particles|depends on the model|any|any|

### Aspect ratios

|V5|V4|niji|testp|
|---|---|---|---|
|any|1:1, 1:2, 2:1, 2:3, 3:2, 4:5, 5:4, 4:7, 7:4, 16:9, 9:16|1:2, 2:1|2:3, 3:2|

### Model properties support

|property|V5|V4|niji|testp|
|---|---|---|---|---|
|model|+|+|+|-|
|type|+|+|-|-|
|renderer|+|+|+|-|
|content|+|+|+|-|
|aspect_ratio|+|+|+|+|
|color|+|+|+|-|
|url|+|+|+|+|

<details>

<summary>

## Results

</summary>

_See more examples in my [gallery](https://github.com/awekrx/MidJourney-Arts)_

### Short-weights model

> prompt: `Sakura blossoms::5, pink flowers::4, Licorice plant::3, Japanese landscape::5, octane render::4, landscape desing::4, red::10, purple::10, , high quality photo::5, soft light::2, sharp-focus::3, hyper realism::4 --v 4 --s 1000 --q 5 --ar 16:9`

![](https://github.com/awekrx/ChatGPT-MidJourney-prompt/blob/master/images/arts/2.png?raw=true)

> prompt: `Stars::5, galaxy::4, space::5, , , , --v 4 --ar 3:2 --s 1000 --q 5 --ar 1:2`

![](https://github.com/awekrx/ChatGPT-MidJourney-prompt/blob/master/images/arts/3.png?raw=true)

## Artistic model

> prompt: `Elven assassin with a masked face and intricate runes. Highly detailed photorealism showcases the intricate details of the mask and runic markings. Focused on the assassin's face, with a blurred background. The lighting is a blend of candlelight and twilight, adding a sense of mystery to the character. The style is a mix of ancient and fantasy. Resolution: --ar 16:9 --s 1000 --q 2 --upbeta --v 4`

![](https://github.com/awekrx/ChatGPT-MidJourney-prompt/blob/master/images/arts/4.png?raw=true)

> prompt: `An elven warrior girl wielding a sword, dressed in armor made of intricate metals and fabrics. She stands against a futuristic background with high-tech elements, rendered with the latest technologies. Focused, blurred background, full-body::5 soft light::1 high quality photo::1 --v 4 --ar 3:2 --s 1000 --q 5`

![](https://github.com/awekrx/ChatGPT-MidJourney-prompt/blob/master/images/arts/5.png?raw=true)

## Niji

> prompt: `Stray dog::3, samurai::5, katana::5, dirt road::3, countryside::3, --niji --q 2`

![](https://github.com/awekrx/ChatGPT-MidJourney-prompt/blob/master/images/arts/1.png?raw=true)

</details>

## License

This project is licensed under the MIT License.

## Acknowledgments

Thanks a lot to the development of AI and separately to [ChatGPT](https://chat.openai.com) for generating the Readme.
And also [acheong08](https://github.com/acheong08) for creating [ChatGPT](https://github.com/acheong08/ChatGPT).

## Future

More advanced options for generating prompts
