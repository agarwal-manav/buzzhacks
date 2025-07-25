import httpx

class TryOnService:
    api_keys = [
        "SG_6a3e0ee83c13a433",
        "SG_9aa0ace1023a2101",
        "SG_c7ef6235f921f150",
        "SG_d5b9ece50252bdf6",
        "SG_57a3fd070c58cd5d",
    ]
    api_key_index = 0
    
    def __init__(self):
        pass

    def try_on(self, product_img_url: str, user_img_url: str, attempt: int = 0):
        """
        curl --location 'https://api.segmind.com/v1/idm-vton' \
            --header 'x-api-key: SG_d5b9ece50252bdf6' \
            --header 'Content-Type: application/json' \
            --data '{
                "crop":false,
                "seed":42,
                "steps":30,
                "category":"upper_body",
                "force_dc":false,
                "human_img":"https://segmind-sd-models.s3.amazonaws.com/display_images/idm-ip.png",
                "garm_img":"https://segmind-sd-models.s3.amazonaws.com/display_images/idm-viton-dress.png",
                "mask_only":false,
                "garment_des":"Green colour semi Formal Blazer"
            }'
        """
        
        # response is a jpeg file. Need to upload to a public url and return the url
        response = httpx.post(
            "https://api.segmind.com/v1/idm-vton",
            headers={
                "x-api-key": self.api_keys[self.api_key_index],
                "Content-Type": "application/json"
            },
            json={
                "crop": False,
                "seed": 42,
                "steps": 30,
                "force_dc": False,
                "human_img": user_img_url,
                "garm_img": product_img_url,
                "mask_only": False
            },
            timeout=100000000
        )
        self.api_key_index = (self.api_key_index + 1) % len(self.api_keys)
        if response.status_code != 200:
            print(f"Failed to try on product after {attempt} attempts")
            if attempt < 3:
                return self.try_on(product_img_url, user_img_url, attempt + 1)
            else:
                raise Exception("Failed to try on product after 3 attempts")

        response = httpx.post(
            "https://api.imgbb.com/1/upload?expiration=600&key=d856a774e50ef4aeb3c9cef89d0e7887",
            files={
                "image": response.content
            },
            timeout=100000000
        )
        return response.json()["data"]["url"]
