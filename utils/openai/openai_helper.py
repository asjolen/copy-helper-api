from utils.subscription.subscription_helper import SubscriptionHelper
from utils.user.user_helper import UserHelper
from recipe.models import Recipes
import os
import openai
import copy


class OpenAIHelper:
    user_helper = UserHelper()
    subscription_helper = SubscriptionHelper()
    api_key = os.environ.get("OPEN_AI_KEY")
    model = "text-davinci-002"
    temperature = 0.75
    max_tokens = 600
    top_p = 1
    frequency_penalty = 1.5
    presence_penalty = 0.8

    def prompt_generator(self, prompt_id, lang, data):
        """
        Replace string variables to the provided values
        """
        recipe = Recipes.objects.filter(id=prompt_id).first()
        prompt_object = recipe.data

        if prompt_object and lang in prompt_object:
            for key in data:
                if key in prompt_object[lang]:
                    prompt_object[lang] = prompt_object[lang].replace("{{" + key + "}}", str(data[key]))

            return prompt_object
        else:
            return False

    def generate(self, request, prompt_id, prompt_language, prompt_data):
        openai.api_key = self.api_key
        responses_list = list()

        prompt = self.prompt_generator(prompt_id=prompt_id, lang=prompt_language, data=prompt_data)

        if prompt and prompt_language in prompt:
            response = openai.Completion.create(
                prompt=prompt[prompt_language],
                model=prompt["model"] if "model" in prompt else self.model,
                temperature=prompt["temperature"] if "temperature" in prompt else self.temperature,
                max_tokens=prompt["max_tokens"] if "max_tokens" in prompt else self.max_tokens,
                top_p=prompt["top_p"] if "top_p" in prompt else self.top_p,
                frequency_penalty=prompt["frequency_penalty"] if "frequency_penalty" in prompt else self.frequency_penalty,
                presence_penalty=prompt["presence_penalty"] if "presence_penalty" in prompt else self.presence_penalty
            )

            self.subscription_helper.record_usage(request, response["usage"]["total_tokens"])

            for response in response["choices"]:
                response["text"] = response["text"].replace("\n", "<alt:end><alt:start>").replace("<alt:end>", "", 1)
                response["text"] = response["text"] + "<alt:end>"

                responses_list.append({
                    "text": response["text"]
                })

        return responses_list

    def replace_nth(self, string, sub, repl, n=1):
        chunks = string.split(sub)
        size = len(chunks)
        rows = size // n + (0 if size % n == 0 else 1)
        return repl.join([
            sub.join([chunks[i * n + j] for j in range(n if (i + 1) * n < size else size - i * n)])
            for i in range(rows)
        ])
