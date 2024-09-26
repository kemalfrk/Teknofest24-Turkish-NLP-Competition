import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from setfit import AbsaModel

app = FastAPI()

class Item(BaseModel):
    text: str = Field(..., example="""Fiber 100mb SuperOnline kullanıcısıyım yaklaşık 2 haftadır @Twitch @Kick_Turkey gibi canlı yayın platformlarında 360p yayın izlerken donmalar yaşıyoruz.  Başka hiç bir operatörler bu sorunu yaşamazken ben parasını verip alamadığım hizmeti neden ödeyeyim ? @Turkcell """)

# Modeli yüklemek icin.
model = AbsaModel.from_pretrained(
    "C:/Users/ryntm/Desktop/model/yarisma-aspect",
    "C:/Users/ryntm/Desktop/model/yarisma-polarity"
)

@app.post("/predict/", response_model=dict)
async def predict(item: Item):
    # Model ile tahmin yapma
    preds = model.predict([item.text])
    print(preds)
    # Sonuçları yeni formata dönüştürme
    result = {
        "entity_list": [],
        "results": []
    }

    # Polarity'yi Türkçe'ye çevirmek için bir eşleştirme
    polarity_map = {
        "positive": "olumlu",
        "negative": "olumsuz",
        "neutral": "nötr"
    }

    # Tahmin edilen verilerin işlenmesi
    for pred in preds:
        for item in pred:
            entity = item['span']
            sentiment = polarity_map[item['polarity']]
            result["results"].append({
                "entity": entity,
                "sentiment": sentiment
            })
            result["entity_list"].append(entity)


    return result

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
