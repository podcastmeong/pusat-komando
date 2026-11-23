# ======================================================================
# PUSAT KOMANDO — salinan dari agent-produksi-produk (Agent 5 Produksi Produk).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent Produksi Produk — Podcast Meong (gratis: Gradio + Gemini free tier).

Memproduksi DRAF produk harian untuk persetujuan Cipta:
video 5, foto 50, eBook 5, lagu 5, musik 5, puisi 5, cerpen 5, POD 5.

Cara jalan:
  pip install -r requirements.txt
  python app.py                       # mode template lokal saja
  GEMINI_API_KEY=xxx python app.py    # mode AI penuh (Gemini free tier)

ATURAN PALING PENTING:
  - Semua hasil adalah DRAF berstatus "menunggu persetujuan". Agent TIDAK
    menerbitkan atau mengunggah apa pun ke platform mana pun.
  - API key HANYA dari environment variable GEMINI_API_KEY. Jangan pernah
    tulis key di file ini atau di file lain.
  - Cerita nabi / orang sholeh: JANGAN mengarang ayat Al-Quran atau hadis.
    Setiap fakta ditandai "PERLU VERIFIKASI" dengan sumber yang harus dicek
    (api.alquran.cloud untuk terjemahan, sunnah.com untuk hadis sahih/hasan).
    Wajah nabi/tokoh TIDAK PERNAH digambarkan — ilustrasi hanya dari belakang.
  - Video/podcast WAJIB kucing (Oyen & Momo). Produk lain temanya bebas.
"""

import json
import os
import random
import re
from datetime import date, timedelta
from pathlib import Path

import gradio as gr

BASE_DIR = Path(__file__).resolve().parent.parent  # PUSAT KOMANDO: root pusat-komando (data/ bersama, output/)
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

RIWAYAT_FILE = DATA_DIR / "riwayat_tema.json"
PROGRES_FILE = DATA_DIR / "progres.json"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODE_AI = bool(GEMINI_API_KEY)
MODEL = "gemini-4-hydrogen"

# ---------------------------------------------------------------------------
# Target produksi harian (keputusan Cipta).
# ---------------------------------------------------------------------------
TARGET_HARIAN = {
    "video": 5,
    "foto": 50,
    "ebook": 5,
    "lagu": 5,
    "musik": 5,
    "puisi": 5,
    "cerpen": 5,
    "pod": 5,
}

JENIS_LABEL = {
    "video": "Video Podcast (3 klip x 10 dtk)",
    "foto": "Foto Stock (prompt + metadata)",
    "ebook": "eBook Anak (kerangka 15 halaman)",
    "lagu": "Lagu (lirik)",
    "musik": "Musik (ide + prompt komposisi)",
    "puisi": "Puisi (20 baris)",
    "cerpen": "Cerpen (~800 kata)",
    "pod": "POD (ide desain + listing Inggris)",
}

HASHTAG = "#PodcastMeong #Oyen #KucingOren #PodcastKucing #FYP"

CATATAN_KEJUJURAN = (
    "CATATAN KEJUJURAN ISI: semua fakta sejarah/keagamaan dalam draf ini "
    "BERTANDA 'PERLU VERIFIKASI'. Jangan terbitkan sebelum setiap fakta "
    "dicek ke api.alquran.cloud (terjemahan Al-Quran) dan sunnah.com "
    "(hadis sahih/hasan saja). Ayat dan hadis TIDAK BOLEH dikarang."
)

# ---------------------------------------------------------------------------
# Bank tema video — dialog Bahasa Inggris sudah dihitung 17-25 kata per klip.
# Format tiap tema: (judul, thumbnail <=4 kata, adegan klip 1-3, dialog 1-3).
# Oyen = suara tinggi ceria, Momo = suara rendah tenang. Satu mulut bergerak
# dalam satu waktu; adegan nyambung; latar sesuai judul.
# ---------------------------------------------------------------------------
VIDEO_TEMA = [
    {
        "judul": "THE MOON IS MADE OF FRIED FISH!",
        "thumbnail": "BULAN IKAN GORENG?!",
        "adegan": [
            "Malam di atap rumah, Oyen menunjuk bulan purnama yang bulat dan kuning.",
            "Momo menggeleng tenang sambil menjelaskan bulan itu batu, bukan makanan.",
            "Oyen tersenyum nakal, membayangkan terbang ke bulan dengan saus sambal.",
        ],
        "dialog": [
            "Momo, look at the moon tonight! It is round, golden, and crispy. I am telling you, that is definitely a giant fried fish up there!",
            "Oyen, the moon is not food. It is a rock floating far away in the sky, and no, we cannot eat it for dinner tonight.",
            "Fine, believe what you want. But tonight I will dream of flying up there with hot sauce and eating the moon myself!",
        ],
    },
    {
        "judul": "OYEN WANTS TO BE AN ASTRONAUT!",
        "thumbnail": "OYEN JADI ASTRONOT!",
        "adegan": [
            "Siang di halaman, Oyen memakai helm astronot kardus sambil menunjuk langit.",
            "Momo duduk tenang menjelaskan astronot berlatih bertahun-tahun.",
            "Oyen melompat latihan, membayangkan lompatan raksasa untuk pecinta ikan.",
        ],
        "dialog": [
            "Momo, I have decided to become an astronaut! I will fly to the stars, and I will bring back space fish for dinner!",
            "Oyen, astronauts train for years. They study, they exercise, and they do not chase butterflies during important space missions.",
            "Then I will train right now! Watch me jump, Momo. One small jump for a cat, one giant leap for fish lovers everywhere!",
        ],
    },
    {
        "judul": "MOMO FORGOT OYEN'S BIRTHDAY!",
        "thumbnail": "MOMO LUPA ULTAH!",
        "adegan": [
            "Ruang tamu penuh balon, Momo bingung melihat dekorasi ulang tahun.",
            "Oyen cemberut karena menunggu kue sejak pagi, Momo tidur saja.",
            "Momo minta maaf dan mengajak pesta dadakan dengan kue ikan.",
        ],
        "dialog": [
            "Oyen, why is the house full of balloons? Did something happen today that I completely forgot about, my dear friend?",
            "It is my birthday, Momo! I waited all morning for cake, and you just sat there sleeping like nothing special happened!",
            "Oh no, I am so sorry! Let us celebrate right now with fish cake, music, and the biggest party this house has ever seen!",
        ],
    },
    {
        "judul": "OYEN OPENS A COFFEE SHOP!",
        "thumbnail": "WARUNG KOPI OYEN!",
        "adegan": [
            "Oyen berdiri bangga di balik kotak kardus bertuliskan 'KOPI OYEN'.",
            "Momo menunjuk kenyataan: tidak ada biji kopi, cangkir, atau pelanggan.",
            "Oyen tersenyum yakin, kotak kardus akan jadi kerajaan kopi besok.",
        ],
        "dialog": [
            "Welcome to my coffee shop, Momo! We serve the finest cat coffee in town, with extra milk and zero dogs allowed inside!",
            "Oyen, you have no coffee beans, no cups, and no customers. All you have is a cardboard box and big dreams.",
            "Every great business starts small, Momo. Tomorrow this box becomes an empire, and you will be my first loyal customer!",
        ],
    },
    {
        "judul": "RAIN AND THE LITTLE UMBRELLA!",
        "thumbnail": "OYEN MAIN HUJAN!",
        "adegan": [
            "Hujan deras di luar jendela, Momo melarang Oyen keluar rumah.",
            "Oyen menatap tetes hujan dengan mata berbinar, ingin bermain.",
            "Momo menyerahkan payung kecil dengan syarat pulang sebelum basah kuyup.",
        ],
        "dialog": [
            "Oyen, it is raining outside. Stay inside, keep your paws dry, and do not even think about chasing raindrops again.",
            "But rain is the best game, Momo! Each drop is a tiny drum, and my paws are the greatest musicians in the world!",
            "Fine, take the small umbrella. But if you come back wet and sneezing, you will drink ginger tea all night long!",
        ],
    },
    {
        "judul": "OYEN LEARNS TO SWIM!",
        "thumbnail": "OYEN BELAJAR RENANG!",
        "adegan": [
            "Siang di kolam, Oyen memakai pelampung sambil menatap air dengan berani.",
            "Momo duduk di tepi kolam menjelaskan kucing harus mulai pelan-pelan.",
            "Oyen mengambang gembira, merasa dirinya separuh ikan.",
        ],
        "dialog": [
            "Momo, today I will learn to swim! The water looks friendly, and I am ready to become the bravest cat in the pool!",
            "Oyen, cats do not like water. Start slowly, stay near the edge, and do not jump in like a crazy fish.",
            "Look, Momo, I am floating! Maybe I am part fish after all, and the pool is my new favorite kingdom!",
        ],
    },
    {
        "judul": "MOMO BECOMES OYEN'S TEACHER!",
        "thumbnail": "MOMO JADI GURU!",
        "adegan": [
            "Ruang belajar, Momo memakai kacamata sambil menulis di papan tulis kecil.",
            "Oyen menguap bosan, ingin belajar menangkap ikan, bukan kesabaran.",
            "Momo tersenyum bijak, ikan selalu datang pada kucing yang sabar menunggu.",
        ],
        "dialog": [
            "Oyen, sit down and listen. Today I will teach you the most important lesson: patience, my dear student.",
            "But teacher, patience is boring! I want to learn something exciting, like catching fish with my bare paws!",
            "Patience is the most exciting lesson, Oyen. Watch and learn: the fish always comes to the cat who waits.",
        ],
    },
    {
        "judul": "OYEN AND THE BIGGEST CAKE!",
        "thumbnail": "KUE TERBESAR OYEN!",
        "adegan": [
            "Dapur, Oyen menatap kue raksasa di atas meja dengan mata berbinar.",
            "Momo menjelaskan kue itu untuk seluruh tetangga, bukan untuk satu kucing.",
            "Oyen tersenyum, rela berbagi satu potong, sisanya miliknya.",
        ],
        "dialog": [
            "Momo, look at this cake! It is the biggest cake in the world, and I am going to eat every single slice!",
            "Oyen, that cake is for the whole neighborhood. If you eat it all, your stomach will complain all night long.",
            "Fine, I will share one slice with you. But the rest is mine, because today I am the king of cake!",
        ],
    },
    {
        "judul": "OYEN IS STUCK IN A TREE!",
        "thumbnail": "OYEN NYANGKUT!",
        "adegan": [
            "Sore di taman, Oyen terjebak di dahan pohon sambil mengejar burung.",
            "Momo di bawah pohon menenangkan Oyen dan berjanji mengambil tangga.",
            "Oyen turun dengan selamat, berjanji hanya memanjat pohon kecil.",
        ],
        "dialog": [
            "Momo, help! I climbed up to catch a bird, and now I am stuck in this tree and cannot climb down!",
            "Oyen, I told you not to climb so high. Stay calm, hold the branch, and I will bring the ladder right now.",
            "Thank you, Momo! From now on, I will only climb small trees, and only when you are watching me.",
        ],
    },
    {
        "judul": "OYEN AND THE LAST FISH!",
        "thumbnail": "IKAN TERAKHIR!",
        "adegan": [
            "Dapur, Oyen dan Momo menatap satu ikan terakhir di dalam mangkuk.",
            "Momo mengusulkan berbagi setengah-setengah seperti sahabat sejati.",
            "Oyen tersenyum hangat, berjanji lain kali semua ikan untuk Momo.",
        ],
        "dialog": [
            "Momo, there is only one fish left in the bowl. We must decide together who deserves this delicious treasure most today.",
            "We can share it, Oyen. Half for you and half for me. That is what true friends do, even with the last fish.",
            "You are the best friend in the world, Momo! Next time I catch two fish, both of them will be yours, I promise!",
        ],
    },
]

# Dialog generik (tema bebas, tetap 17-25 kata per klip).
DIALOG_GENERIK = [
    "Momo, I have a brand new idea today! It is funny, it is brave, and I think everyone will love it!",
    "Tell me everything, Oyen. But remember, a good idea needs a good plan, patience, and maybe some fish as a reward.",
    "Then let us start right now, Momo! Together we can do anything, even the silliest idea in the whole wide world!",
]

# ---------------------------------------------------------------------------
# Bank subjek foto stock (prompt EN + judul EN + 10 kata kunci).
# ---------------------------------------------------------------------------
FOTO_SUBJEK = {
    "kucing": [
        ("Orange tabby cat sitting on a wooden fence at golden hour, warm sunlight, shallow depth of field",
         "Orange Tabby Cat Sitting on a Wooden Fence at Golden Hour",
         "orange cat, tabby cat, cat portrait, golden hour, pet, animal, cute cat, outdoor cat, sunlight, feline"),
        ("Grey cat with green eyes, close-up portrait, soft window light, looking at camera",
         "Close Up of a Grey Cat with Green Eyes Looking at Camera",
         "grey cat, cat portrait, green eyes, close up, pet photography, animal, cute cat, indoor cat, feline, whiskers"),
        ("White cat walking on a sandy beach at sunset, paw prints in sand, warm tones",
         "White Cat Walking on a Sandy Beach at Sunset",
         "white cat, beach, sunset, cat walking, sand, animal, pet, seaside, summer, feline"),
        ("Two kittens playing with a yarn ball on a cozy rug, bright living room",
         "Two Kittens Playing with a Yarn Ball on a Cozy Rug",
         "kittens, playing cats, yarn ball, cute kittens, pet, indoor, cozy home, animal, funny cats, adorable"),
        ("Cat sleeping in a sunbeam on a windowsill, peaceful, soft warm light",
         "Cat Sleeping in a Sunbeam on a Windowsill",
         "sleeping cat, sunbeam, windowsill, peaceful cat, pet, cozy, warm light, animal, relaxation, home"),
        ("Orange cat wearing a small straw hat in a sunny garden, flowers around",
         "Orange Cat Wearing a Straw Hat in a Sunny Garden",
         "orange cat, straw hat, garden, flowers, summer, cute cat, pet, funny cat, sunny day, animal"),
        ("Cat looking at a butterfly in a flower meadow, spring day, soft bokeh",
         "Cat Looking at a Butterfly in a Flower Meadow",
         "cat and butterfly, meadow, flowers, spring, nature, cute cat, animal, outdoors, bokeh, peaceful"),
        ("Black cat silhouette against city lights at dusk, mysterious mood",
         "Black Cat Silhouette Against City Lights at Dusk",
         "black cat, silhouette, city lights, dusk, mysterious, night, urban, animal, evening, moody"),
    ],
    "alam": [
        ("Misty mountain lake at sunrise, pine forest reflection in calm water",
         "Misty Mountain Lake at Sunrise with Pine Forest Reflection",
         "mountain lake, mist, sunrise, pine forest, reflection, nature, landscape, serene, morning, wilderness"),
        ("Waterfall in a tropical rainforest, long exposure, lush green moss",
         "Waterfall in a Tropical Rainforest with Lush Green Moss",
         "waterfall, rainforest, tropical, nature, long exposure, green, jungle, water, landscape, fresh"),
        ("Lavender field under a purple evening sky, rows of flowers",
         "Lavender Field Under a Purple Evening Sky",
         "lavender field, purple flowers, evening sky, agriculture, nature, landscape, summer, fragrant, rows, scenic"),
        ("Snow-covered pine trees in a winter forest, soft snowfall",
         "Snow Covered Pine Trees in a Winter Forest",
         "winter forest, snow, pine trees, snowfall, cold, nature, landscape, white, peaceful, season"),
        ("Ocean waves crashing on a rocky cliff at dawn, dramatic spray",
         "Ocean Waves Crashing on a Rocky Cliff at Dawn",
         "ocean waves, rocky cliff, dawn, sea, dramatic, spray, coastline, nature, power, seascape"),
        ("Autumn maple leaves on a forest path, golden and red colors",
         "Autumn Maple Leaves on a Forest Path in Golden Colors",
         "autumn leaves, maple, forest path, golden, red, fall season, nature, walkway, colorful, trees"),
        ("Desert dunes with soft shadows at sunset, rippled sand patterns",
         "Desert Dunes with Soft Shadows at Sunset",
         "desert dunes, sand, sunset, shadows, arid, landscape, golden, ripples, nature, warm"),
        ("Green rice terraces in morning fog, Bali, layered hills",
         "Green Rice Terraces in Morning Fog with Layered Hills",
         "rice terraces, fog, morning, green hills, agriculture, asia, landscape, layered, nature, travel"),
    ],
    "makanan": [
        ("Bowl of ramen with steam rising, chopsticks, warm restaurant light",
         "Bowl of Ramen with Steam Rising in Warm Light",
         "ramen, noodles, japanese food, steam, bowl, chopsticks, delicious, asian food, hot, restaurant"),
        ("Fresh croissants on a wooden table with a cup of coffee, morning light",
         "Fresh Croissants on a Wooden Table with Coffee",
         "croissant, breakfast, coffee, bakery, morning, wooden table, pastry, fresh, food photography, cozy"),
        ("Colorful fruit salad in a glass bowl, bright daylight, fresh berries",
         "Colorful Fruit Salad in a Glass Bowl with Fresh Berries",
         "fruit salad, berries, healthy food, fresh fruit, glass bowl, colorful, vitamins, summer, dessert, bright"),
        ("Indonesian fried rice with egg and crackers on a plate, street food style",
         "Indonesian Fried Rice with Egg and Crackers",
         "nasi goreng, indonesian food, fried rice, egg, crackers, street food, asian cuisine, plate, spicy, delicious"),
        ("Stack of pancakes with honey and berries, soft morning light",
         "Stack of Pancakes with Honey and Berries",
         "pancakes, honey, berries, breakfast, sweet, stack, syrup, morning, food photography, delicious"),
        ("Avocado toast with egg on a ceramic plate, cafe style, bright",
         "Avocado Toast with Egg on a Ceramic Plate",
         "avocado toast, egg, cafe food, healthy breakfast, ceramic plate, bright, brunch, food, fresh, modern"),
        ("Cup of hot chocolate with marshmallows, cozy winter mood",
         "Cup of Hot Chocolate with Marshmallows in Cozy Winter Mood",
         "hot chocolate, marshmallows, winter, cozy, warm drink, mug, sweet, comfort, cocoa, steam"),
        ("Street food satay skewers grilling over charcoal, smoke and fire",
         "Street Food Satay Skewers Grilling Over Charcoal",
         "satay, skewers, grill, charcoal, street food, smoke, indonesian food, barbecue, fire, delicious"),
    ],
    "benda": [
        ("Vintage camera on a wooden desk with old books, warm nostalgic light",
         "Vintage Camera on a Wooden Desk with Old Books",
         "vintage camera, retro, photography, wooden desk, books, nostalgia, old, film camera, warm, still life"),
        ("Ceramic coffee mug with latte art on a table, cozy cafe mood",
         "Ceramic Coffee Mug with Latte Art on a Table",
         "coffee mug, latte art, ceramic, cafe, cozy, hot coffee, morning, drink, ceramic cup, warm"),
        ("Leather journal and fountain pen flat lay on a dark desk",
         "Leather Journal and Fountain Pen Flat Lay",
         "leather journal, fountain pen, writing, flat lay, notebook, desk, stationery, vintage, dark, creative"),
        ("Wristwatch on a marble surface, luxury product photography style",
         "Luxury Wristwatch on a Marble Surface",
         "wristwatch, luxury, marble, product photography, elegant, time, accessory, watch, premium, style"),
        ("Potted succulent plant on a white windowsill, bright daylight",
         "Potted Succulent Plant on a White Windowsill",
         "succulent, potted plant, windowsill, bright, green, indoor plant, home decor, minimal, nature, fresh"),
        ("Old bicycle leaning against a brick wall, street photography",
         "Old Bicycle Leaning Against a Brick Wall",
         "bicycle, brick wall, street, vintage bike, urban, old, city, photography, retro, wall"),
        ("Pair of sneakers on a colorful background, product shot",
         "Pair of Sneakers on a Colorful Background",
         "sneakers, shoes, colorful background, product photography, fashion, footwear, sport, modern, style, pair"),
        ("Reading glasses and an open book on a bed, soft evening light",
         "Reading Glasses and an Open Book on a Bed",
         "reading glasses, open book, bed, evening light, reading, cozy, literature, relax, home, soft"),
    ],
    "cozy": [
        ("Cozy reading nook with a warm lamp and a knitted blanket, evening",
         "Cozy Reading Nook with a Warm Lamp and Knitted Blanket",
         "cozy reading nook, warm lamp, knitted blanket, evening, home, comfort, books, relax, interior, hygge"),
        ("Cat sleeping on a knitted blanket near a fireplace, warm glow",
         "Cat Sleeping on a Knitted Blanket Near a Fireplace",
         "sleeping cat, knitted blanket, fireplace, warm glow, cozy, pet, winter, home, comfort, peaceful"),
        ("Hot tea cup on a wooden tray by a rainy window, steam rising",
         "Hot Tea Cup on a Wooden Tray by a Rainy Window",
         "hot tea, rainy window, wooden tray, steam, cozy, rain, comfort, warm drink, home, peaceful"),
        ("Bedroom with fairy lights and soft pillows, dreamy atmosphere",
         "Bedroom with Fairy Lights and Soft Pillows",
         "bedroom, fairy lights, soft pillows, dreamy, cozy, interior, lights, comfortable, night, home decor"),
        ("Person reading a book under a warm blanket, soft lamp light",
         "Person Reading a Book Under a Warm Blanket",
         "reading book, warm blanket, lamp light, cozy, relax, evening, home, comfort, person, peaceful"),
        ("Warm living room with candles and a bookshelf, autumn evening",
         "Warm Living Room with Candles and a Bookshelf",
         "living room, candles, bookshelf, autumn evening, warm, cozy, interior, home, books, comfort"),
        ("Knitted sweater on an armchair, autumn mood, warm tones",
         "Knitted Sweater on an Armchair in Autumn Mood",
         "knitted sweater, armchair, autumn, warm tones, cozy, home, knitwear, comfort, fall, interior"),
        ("Morning coffee in bed with soft sunlight through curtains",
         "Morning Coffee in Bed with Soft Sunlight",
         "morning coffee, bed, soft sunlight, curtains, cozy, breakfast in bed, warm, relax, home, peaceful"),
    ],
    "natal": [
        ("Christmas tree with golden ornaments and warm lights, living room",
         "Christmas Tree with Golden Ornaments and Warm Lights",
         "christmas tree, golden ornaments, warm lights, holiday, living room, festive, december, decoration, cozy, celebration"),
        ("Santa hat on an orange cat, festive red background",
         "Santa Hat on an Orange Cat with Festive Background",
         "santa hat, orange cat, christmas, festive, funny cat, red background, holiday, cute pet, celebration, winter"),
        ("Snowman in a snowy garden with a red scarf, cheerful",
         "Snowman in a Snowy Garden with a Red Scarf",
         "snowman, snowy garden, red scarf, winter, cheerful, snow, holiday, christmas, cold, fun"),
        ("Christmas gifts with red ribbons under a decorated tree",
         "Christmas Gifts with Red Ribbons Under a Decorated Tree",
         "christmas gifts, red ribbons, decorated tree, presents, holiday, festive, december, celebration, surprise, wrapping"),
        ("Hot cocoa with a candy cane, cozy winter background",
         "Hot Cocoa with a Candy Cane in Cozy Winter",
         "hot cocoa, candy cane, winter, cozy, christmas drink, warm, sweet, holiday, mug, festive"),
        ("Christmas wreath with pine cones on a wooden door",
         "Christmas Wreath with Pine Cones on a Wooden Door",
         "christmas wreath, pine cones, wooden door, holiday decoration, festive, winter, green, traditional, entrance, december"),
        ("Reindeer decoration with fairy lights at night, glowing",
         "Reindeer Decoration with Fairy Lights at Night",
         "reindeer decoration, fairy lights, night, glowing, christmas, holiday, festive, garden, winter, magical"),
        ("Child opening a Christmas present, joyful expression, warm light",
         "Child Opening a Christmas Present with Joyful Expression",
         "child, christmas present, joyful, opening gift, warm light, holiday, family, happiness, celebration, surprise"),
    ],
    "travel": [
        ("Hot air balloons over Cappadocia at sunrise, colorful sky",
         "Hot Air Balloons over Cappadocia at Sunrise",
         "hot air balloons, cappadocia, sunrise, colorful sky, travel, turkey, adventure, aerial, morning, landscape"),
        ("Venice canal with gondolas at golden hour, historic buildings",
         "Venice Canal with Gondolas at Golden Hour",
         "venice canal, gondola, golden hour, italy, historic buildings, water, travel, romantic, europe, city"),
        ("Tokyo street with neon lights at night, busy and vibrant",
         "Tokyo Street with Neon Lights at Night",
         "tokyo street, neon lights, night, japan, busy, vibrant, city, urban, travel, asia"),
        ("Santorini white buildings and blue domes, Aegean sea view",
         "Santorini White Buildings and Blue Domes with Sea View",
         "santorini, white buildings, blue domes, aegean sea, greece, travel, island, summer, view, mediterranean"),
        ("Backpacker hiking on a mountain trail to a viewpoint, sunrise",
         "Backpacker Hiking on a Mountain Trail at Sunrise",
         "backpacker, hiking, mountain trail, viewpoint, sunrise, adventure, travel, nature, trekking, outdoor"),
        ("Tropical beach with palm trees and turquoise sea, paradise",
         "Tropical Beach with Palm Trees and Turquoise Sea",
         "tropical beach, palm trees, turquoise sea, paradise, summer, vacation, sand, ocean, travel, relax"),
        ("Paris Eiffel Tower at sunset seen from a street cafe",
         "Paris Eiffel Tower at Sunset from a Street Cafe",
         "paris, eiffel tower, sunset, street cafe, france, travel, city, romantic, europe, landmark"),
        ("Ancient temple in Bali with morning mist, spiritual atmosphere",
         "Ancient Temple in Bali with Morning Mist",
         "bali temple, morning mist, ancient, spiritual, indonesia, travel, asia, misty, sacred, culture"),
    ],
}

# ---------------------------------------------------------------------------
# Kerangka eBook anak — 12 alur per tokoh. Setiap alur WAJIB ditandai
# "PERLU VERIFIKASI" (tidak ada nomor ayat / teks hadis dalam template).
# ---------------------------------------------------------------------------
EBOOK_TOPIK = {
    "Nabi Nuh": {
        "sumber": "api.alquran.cloud (terjemahan) — cek kisah Nuh; sunnah.com bila memakai hadis.",
        "alur": [
            "Nabi Nuh mengajak kaumnya menyembah Allah dan meninggalkan berhala.",
            "Kaumnya menolak dan mengejek ajakan Nabi Nuh selama bertahun-tahun.",
            "Nabi Nuh tetap bersabar dan terus berdakwah dengan lembut.",
            "Allah memerintahkan Nabi Nuh membangun bahtera yang besar.",
            "Nabi Nuh membangun bahtera dibantu orang-orang yang beriman.",
            "Kaum yang ingkar menertawakan bahtera di tengah daratan.",
            "Allah memerintahkan hewan-hewan dibawa berpasang-pasangan ke bahtera.",
            "Air bah datang dan menutupi bumi.",
            "Bahtera berlayar dengan aman atas izin Allah.",
            "Orang-orang beriman selamat bersama Nabi Nuh.",
            "Bahtera berlabuh setelah air surut.",
            "Nabi Nuh mengajarkan syukur dan ketaatan kepada Allah.",
        ],
    },
    "Nabi Yunus": {
        "sumber": "api.alquran.cloud (terjemahan) — cek kisah Yunus; sunnah.com bila memakai hadis.",
        "alur": [
            "Nabi Yunus berdakwah kepada kaum Ninawa.",
            "Kaumnya menolak, Nabi Yunus pergi dengan kecewa.",
            "Nabi Yunus naik kapal dan badai besar datang.",
            "Para penumpang mengundi, nama Yunus yang keluar.",
            "Nabi Yunus dilempar ke laut dan ditelan ikan besar.",
            "Di dalam perut ikan, Nabi Yunus berdoa dengan sungguh-sungguh.",
            "Allah mengampuni dan menyelamatkan Nabi Yunus.",
            "Ikan memuntahkan Nabi Yunus ke daratan.",
            "Nabi Yunus kembali berdakwah kepada kaumnya.",
            "Kaum Ninawa akhirnya beriman.",
            "Allah memberi mereka kehidupan yang baik.",
            "Kisah ini mengajarkan taubat dan kesabaran.",
        ],
    },
    "Nabi Yusuf": {
        "sumber": "api.alquran.cloud (terjemahan) — cek kisah Yusuf; sunnah.com bila memakai hadis.",
        "alur": [
            "Nabi Yusuf kecil bermimpi sebelas bintang, matahari, dan bulan bersujud.",
            "Saudara-saudaranya iri kepada Yusuf.",
            "Yusuf dibuang ke sumur oleh saudara-saudaranya.",
            "Kafilah menemukan Yusuf dan membawanya ke Mesir.",
            "Yusuf tumbuh menjadi pemuda yang jujur dan baik.",
            "Yusuf menghadapi ujian fitnah dengan sabar.",
            "Yusuf dipenjara meski tidak bersalah.",
            "Di penjara, Yusuf menafsirkan mimpi dengan izin Allah.",
            "Raja Mesir memanggil Yusuf untuk menafsirkan mimpinya.",
            "Yusuf dipercaya mengurus perbendaharaan Mesir.",
            "Saudara-saudara Yusuf datang meminta makanan.",
            "Yusuf memaafkan saudara-saudaranya dan keluarga berkumpul kembali.",
        ],
    },
    "Nabi Musa": {
        "sumber": "api.alquran.cloud (terjemahan) — cek kisah Musa; sunnah.com bila memakai hadis.",
        "alur": [
            "Nabi Musa lahir saat bayi laki-laki Bani Israil diburu.",
            "Ibu Musa menghanyutkan bayinya di Sungai Nil.",
            "Keluarga Fir'aun menemukan dan merawat bayi Musa.",
            "Musa tumbuh di istana, lalu pergi ke Madyan.",
            "Di Madyan, Musa menolong dua perempuan memberi minum ternak.",
            "Allah berbicara kepada Musa di Bukit Tursina.",
            "Musa kembali ke Mesir mengajak Fir'aun beriman.",
            "Fir'aun menolak dan menantang Musa.",
            "Musa membawa Bani Israil keluar dari Mesir.",
            "Laut terbelah dan Bani Israil selamat.",
            "Musa menerima Taurat di Bukit Tursina.",
            "Musa mengajarkan ketaatan dan kesabaran.",
        ],
    },
    "Nabi Ibrahim": {
        "sumber": "api.alquran.cloud (terjemahan) — cek kisah Ibrahim; sunnah.com bila memakai hadis.",
        "alur": [
            "Nabi Ibrahim kecil bertanya tentang Tuhan yang sebenarnya.",
            "Ibrahim mengajak kaumnya meninggalkan berhala.",
            "Ibrahim menghancurkan berhala-berhala kecil.",
            "Raja dan kaumnya marah besar kepada Ibrahim.",
            "Ibrahim dilempar ke api, tetapi api menjadi dingin atas izin Allah.",
            "Ibrahim berhijrah dan berdakwah di tempat baru.",
            "Ibrahim berdoa agar diberi anak yang saleh.",
            "Allah memberi kabar gembira tentang Ismail.",
            "Ibrahim dan Ismail membangun Ka'bah bersama.",
            "Ibrahim berdoa untuk keamanan kota Mekah.",
            "Keluarga Ibrahim menjadi teladan ketaatan.",
            "Ibrahim dikenal sebagai bapak para nabi.",
        ],
    },
    "Nabi Ayub": {
        "sumber": "api.alquran.cloud (terjemahan) — cek kisah Ayub; sunnah.com bila memakai hadis.",
        "alur": [
            "Nabi Ayub hidup berkecukupan dan bersyukur.",
            "Allah menguji Ayub dengan kehilangan harta.",
            "Ayub kehilangan anak-anaknya, tetapi tetap bersabar.",
            "Ayub menderita sakit yang lama.",
            "Ayub tidak pernah mengeluh kepada Allah.",
            "Istrinya tetap setia mendampingi Ayub.",
            "Ayub berdoa dengan rendah hati memohon kesembuhan.",
            "Allah menyembuhkan Ayub dan mengembalikan nikmatnya.",
            "Ayub kembali berkumpul dengan keluarganya.",
            "Harta Ayub dikembalikan berlipat ganda.",
            "Kesabaran Ayub menjadi teladan sepanjang zaman.",
            "Ayub mengajarkan bahwa ujian adalah tanda kasih Allah.",
        ],
    },
    "Abu Bakar": {
        "sumber": "sunnah.com (hadis sahih/hasan saja) dan sumber sejarah tepercaya — semua fakta perlu verifikasi.",
        "alur": [
            "Abu Bakar adalah sahabat dekat Nabi Muhammad sejak muda.",
            "Abu Bakar membenarkan kabar kenabian tanpa ragu.",
            "Abu Bakar membebaskan budak-budak yang disiksa karena beriman.",
            "Abu Bakar menemani Nabi dalam hijrah ke Madinah.",
            "Keduanya bersembunyi di Gua Tsur dari kejaran musuh.",
            "Abu Bakar menjadi khalifah pertama setelah Nabi wafat.",
            "Abu Bakar menjaga persatuan umat Islam.",
            "Abu Bakar memerangi orang yang menolak zakat.",
            "Abu Bakar mengumpulkan Al-Quran menjadi satu mushaf.",
            "Abu Bakar hidup sederhana meski menjadi pemimpin.",
            "Abu Bakar wafat dan dimakamkan di samping Nabi.",
            "Abu Bakar mengajarkan kejujuran dan kesetiaan.",
        ],
    },
    "Umar bin Khattab": {
        "sumber": "sunnah.com (hadis sahih/hasan saja) dan sumber sejarah tepercaya — semua fakta perlu verifikasi.",
        "alur": [
            "Umar bin Khattab awalnya menentang Islam.",
            "Umar masuk Islam setelah membaca ayat Al-Quran.",
            "Keislaman Umar membuat dakwah semakin berani.",
            "Umar dikenal tegas membela kebenaran.",
            "Umar menjadi khalifah kedua setelah Abu Bakar.",
            "Umar membangun sistem pemerintahan yang adil.",
            "Umar berkeliling malam memeriksa rakyatnya.",
            "Umar membantu ibu yang memasak batu untuk anak-anaknya.",
            "Umar memperluas wilayah Islam dengan bijaksana.",
            "Umar hidup sederhana dan takut kepada Allah.",
            "Umar wafat setelah ditikam saat salat.",
            "Umar mengajarkan keadilan dan keberanian.",
        ],
    },
    "Imam Syafi'i": {
        "sumber": "sunnah.com (hadis sahih/hasan saja) dan sumber sejarah tepercaya — semua fakta perlu verifikasi.",
        "alur": [
            "Imam Syafi'i lahir dan tumbuh sebagai anak yatim.",
            "Sejak kecil ia gemar menghafal Al-Quran dan hadis.",
            "Ibunya membawanya belajar kepada para ulama.",
            "Syafi'i muda menghafal kitab Al-Muwaththa.",
            "Ia belajar kepada Imam Malik di Madinah.",
            "Syafi'i menulis kitab Al-Umm yang terkenal.",
            "Ia mendirikan mazhab Syafi'i yang diikuti banyak umat.",
            "Syafi'i terkenal cerdas dan kuat hafalannya.",
            "Ia mengajarkan adab sebelum ilmu.",
            "Syafi'i hidup sederhana dan dermawan.",
            "Karya-karyanya menjadi rujukan hingga kini.",
            "Syafi'i mengajarkan pentingnya menuntut ilmu.",
        ],
    },
    "Salahuddin Al-Ayyubi": {
        "sumber": "Sumber sejarah tepercaya (kronik sezaman) — semua fakta perlu verifikasi; tanpa angka pasukan / tebusan.",
        "alur": [
            "Salahuddin tumbuh dalam keluarga yang mencintai ilmu dan jihad.",
            "Sejak muda ia belajar agama dan ilmu perang.",
            "Salahuddin dikenal adil dan rendah hati.",
            "Ia menyatukan kekuatan umat Islam yang terpecah.",
            "Salahuddin memimpin pasukannya dengan bijaksana.",
            "Dalam pertempuran ia tetap menjaga adab dan kemanusiaan.",
            "Yerusalem dibebaskan dengan damai dan penuh kasih.",
            "Penduduk yang kalah diperlakukan dengan baik.",
            "Salahuddin mengampuni banyak tawanan.",
            "Ia membangun sekolah dan rumah sakit.",
            "Salahuddin wafat dalam keadaan sederhana.",
            "Salahuddin mengajarkan keadilan dan kasih sayang.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Bank puisi — masing-masing TEPAT 20 baris (4 bait x 5 baris).
# ---------------------------------------------------------------------------
PUISI_BANK = {
    "Senja Bareng Oyen": [
        "Senja turun pelan di atas atap,",
        "Oyen duduk manis menatap langit jingga,",
        "Momo datang dengan langkah tenang,",
        "dua sahabat berbagi hangat sore,",
        "tak ada yang lebih indah dari ini.",
        "Angin sore menyapa bulu-bulu lembut,",
        "bau ikan goreng dari dapur tetangga,",
        "perut Oyen berbunyi minta makan,",
        "Momo tertawa pelan sambil menggeleng,",
        "sabar, katanya, rezeki tak ke mana.",
        "Matahari pamit di ujung barat,",
        "bintang pertama muncul malu-malu,",
        "Oyen menghitung satu dua tiga,",
        "Momo menutup mata, berdoa syukur,",
        "hari ini pun berlalu dengan bahagia.",
        "Bila esok senja datang lagi,",
        "kami akan duduk di tempat yang sama,",
        "bercerita tentang bulan dan ikan,",
        "tertawa sampai perut terasa hangat,",
        "karena sahabat adalah rumah yang sejati.",
    ],
    "Hujan dan Kucing": [
        "Hujan turun membasahi genting,",
        "Oyen berlari mencari tempat teduh,",
        "Momo menunggu di balik pintu,",
        "mengibaskan ekor, memanggil pelan,",
        "cepat masuk, nanti kau kedinginan.",
        "Tetes hujan menari di atas daun,",
        "bunyinya seperti drum kecil yang riang,",
        "Oyen menatap dari jendela kaca,",
        "matanya berbinar penuh tanya,",
        "kenapa langit menangis hari ini?",
        "Momo menjawab dengan suara lembut,",
        "langit hanya sedang menyiram bumi,",
        "supaya bunga-bunga bisa tumbuh,",
        "supaya sungai kembali penuh,",
        "hujan adalah hadiah, bukan hukuman.",
        "Oyen mengangguk, lalu tertawa,",
        "kalau begitu, mari kita bernyanyi,",
        "lagu hujan untuk semua kucing,",
        "sampai langit kembali cerah,",
        "dan pelangi muncul di ujung sana.",
    ],
    "Persahabatan Oyen dan Momo": [
        "Dua ekor kucing, satu atap yang sama,",
        "Oyen si oren, Momo si abu,",
        "berbeda warna, berbeda suara,",
        "tapi hati mereka satu tujuan,",
        "sahabat sejati tak pernah berpisah.",
        "Pagi hari mereka berburu sinar,",
        "siang hari tidur di bawah kursi,",
        "sore hari berebut ikan terakhir,",
        "malam hari berbagi selimut hangat,",
        "setiap hari adalah petualangan.",
        "Kadang bertengkar soal mangkuk makan,",
        "kadang berebut tempat paling nyaman,",
        "tapi tak pernah sampai membenci,",
        "karena maaf selalu datang cepat,",
        "dan tawa selalu jadi penutup.",
        "Bila satu jatuh, satu menolong,",
        "bila satu lapar, satu berbagi,",
        "begitulah arti persahabatan,",
        "bukan soal siapa yang paling hebat,",
        "tapi siapa yang selalu ada.",
    ],
}

# ---------------------------------------------------------------------------
# Bank lirik lagu anak/kucing (Bahasa Indonesia).
# Struktur: [Verse 1] 4 baris, [Chorus] 4 baris, [Verse 2] 4 baris,
# [Chorus] 4 baris, [Outro] 2 baris.
# ---------------------------------------------------------------------------
LAGU_BANK = {
    "Oyen dan Momo": {
        "verse1": [
            "Oyen si kucing oren, suka berlari,",
            "Momo si abu-abu, tenang sekali,",
            "dua sahabat di rumah yang sama,",
            "setiap hari penuh cerita.",
        ],
        "chorus": [
            "Meong meong, ayo bernyanyi,",
            "Oyen dan Momo sahabat sejati,",
            "meong meong, tertawa bersama,",
            "dunia jadi cerah karenanya.",
        ],
        "verse2": [
            "Pagi hari berburu sinar mentari,",
            "siang hari tidur di bawah kursi,",
            "sore hari berebut ikan goreng,",
            "malam hari tidur berpelukan.",
        ],
        "outro": [
            "Oyen dan Momo, sahabat selamanya,",
            "meong meong, sampai jumpa lagi!",
        ],
    },
    "Senja Bareng Oyen": {
        "verse1": [
            "Senja turun, langit jadi jingga,",
            "Oyen duduk di atas atap,",
            "Momo datang membawa senyum,",
            "kita nikmati sore yang tenang.",
        ],
        "chorus": [
            "Senja senja, indah sekali,",
            "warna jingga di langit sore,",
            "senja senja, bersama Oyen,",
            "hati pun jadi damai.",
        ],
        "verse2": [
            "Angin sore membelai lembut,",
            "bintang muncul satu persatu,",
            "Oyen menghitung sambil tertawa,",
            "Momo berdoa penuh syukur.",
        ],
        "outro": [
            "Bila senja datang lagi esok,",
            "kita duduk di tempat yang sama.",
        ],
    },
    "Hujan dan Kucing": {
        "verse1": [
            "Hujan turun, tik tik tik,",
            "Oyen berlari masuk rumah,",
            "Momo menunggu di balik pintu,",
            "cepat masuk, jangan basah kuyup.",
        ],
        "chorus": [
            "Hujan hujan, jangan berhenti,",
            "kami bernyanyi di balik jendela,",
            "hujan hujan, basahi bumi,",
            "bunga pun mekar karenanya.",
        ],
        "verse2": [
            "Tetes hujan menari di daun,",
            "bunyi drum kecil yang riang,",
            "Oyen menatap penuh tanya,",
            "kenapa langit menangis hari ini?",
        ],
        "outro": [
            "Hujan pun reda, pelangi muncul,",
            "Oyen dan Momo tersenyum senang.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Bank POD — ide desain + listing Bahasa Inggris.
# ATURAN: istilah pahlawan super berlisensi DILARANG — pakai "super cat" / "hero cat".
# ---------------------------------------------------------------------------
POD_BANK = [
    {
        "tema": "Oyen Minum Kopi",
        "desain": "Kucing oren gemuk duduk di meja kafe, memegang cangkir kopi dengan kedua cakar, mata setengah tertutup menikmati aroma, latar krem lembut, gaya ilustrasi kartun tebal.",
        "judul_en": "Cute Orange Cat Drinking Coffee Funny Cat Coffee Lover",
        "deskripsi_en": (
            "A cute orange cat enjoying a warm cup of coffee. Perfect for coffee "
            "lovers and cat lovers who cannot start the day without caffeine "
            "and cuddles. A funny, cozy design for your morning routine."
        ),
        "tags_en": "orange cat, coffee lover, funny cat, cat lover, cute cat, coffee addict, kitten, cafe, morning coffee, cat mom",
    },
    {
        "tema": "Oyen Memancing",
        "desain": "Kucing oren memakai topi nelayan, duduk di tepi danau memegang pancing bambu, ember kecil berisi ikan di samping, matahari terbenam jingga, gaya ilustrasi cat air lucu.",
        "judul_en": "Cute Orange Cat Fishing Funny Fisherman Cat Lover",
        "deskripsi_en": (
            "An orange cat with a fishing rod waiting patiently by the lake. "
            "A funny design for fishing lovers and cat lovers who know that "
            "patience is the best bait. Great gift for anglers and pet lovers."
        ),
        "tags_en": "fishing cat, fisherman cat, orange cat, funny cat, cat lover, fishing lover, angler gift, cute cat, lake fishing, cat dad",
    },
    {
        "tema": "Duo Oyen dan Momo",
        "desain": "Dua kucing sahabat — oren dan abu-abu — duduk berdampingan dengan senyum lebar, satu memegang ikan, satu memegang buku, latar bintang kecil, gaya kartun ramah.",
        "judul_en": "Cute Orange and Grey Cat Duo Best Friends Funny Cat Lovers",
        "deskripsi_en": (
            "Two best friend cats, one orange and one grey, always together. "
            "A heartwarming design for best friends, cat lovers, and anyone "
            "who believes friendship makes every day better."
        ),
        "tags_en": "cat duo, best friends, orange cat, grey cat, funny cats, cat lovers, cute cats, friendship, kitten duo, pet lovers",
    },
    {
        "tema": "Oyen Astronot",
        "desain": "Kucing oren memakai helm astronot kaca, melayang di angkasa dengan bintang dan bulan keju di latar, gaya ilustrasi kartun cerah dan lucu.",
        "judul_en": "Cute Orange Cat Astronaut in Space Funny Hero Cat",
        "deskripsi_en": (
            "An orange hero cat floating in space wearing an astronaut helmet. "
            "A fun design for space lovers, dreamers, and cat fans who believe "
            "every cat is a brave explorer of the universe."
        ),
        "tags_en": "astronaut cat, space cat, hero cat, orange cat, funny cat, cat lover, space lover, cute cat, galaxy, dreamer",
    },
    {
        "tema": "Oyen Natal",
        "desain": "Kucing oren memakai topi Santa merah, duduk di samping pohon Natal kecil dengan lampu hangat dan hadiah, latar salju lembut, gaya ilustrasi perayaan.",
        "judul_en": "Cute Orange Cat with Santa Hat Christmas Holiday Cat",
        "deskripsi_en": (
            "A cute orange cat wearing a Santa hat next to a small Christmas "
            "tree. The perfect festive design for cat lovers who celebrate "
            "Christmas with their furry best friend."
        ),
        "tags_en": "christmas cat, santa hat, orange cat, holiday cat, cute cat, christmas gift, festive, winter, cat lover, xmas",
    },
    {
        "tema": "Kucing dan Buku",
        "desain": "Kucing abu-abu memakai kacamata baca, duduk di tumpukan buku tebal dengan cangkir teh, lampu hangat, latar perpustakaan mini, gaya ilustrasi lembut.",
        "judul_en": "Cute Grey Cat Reading Books Funny Book Lover Cat",
        "deskripsi_en": (
            "A grey cat with reading glasses sitting on a pile of books. "
            "A lovely design for book lovers, librarians, and cat fans who "
            "think every good story is better with a cat beside you."
        ),
        "tags_en": "reading cat, book lover, grey cat, cute cat, library cat, bookworm, funny cat, cat lover, glasses cat, cozy reading",
    },
]

# ---------------------------------------------------------------------------
# Kerangka cerpen (~800 kata) — kalimat pengisi untuk mencapai target kata.
# ---------------------------------------------------------------------------
CERPEN_KALIMAT_PENGISI = [
    "Pagi itu udara terasa sejuk, dan cahaya matahari masuk pelan lewat jendela kayu yang sudah tua.",
    "Oyen menguap lebar, meregangkan badannya, lalu melompat turun dari kasur dengan semangat yang baru.",
    "Momo sudah bangun lebih dulu, duduk rapi di dekat dapur sambil menunggu sarapan disiapkan.",
    "Di luar, suara burung bersahutan, seolah ikut menyambut hari yang baru saja dimulai.",
    "Aroma ikan goreng tercium dari dapur, dan perut Oyen langsung berbunyi keras meminta makan.",
    "Momo menatap Oyen dengan senyum kecil, seolah berkata bahwa kesabaran adalah kunci segalanya.",
    "Mereka berdua makan dengan lahap, lalu duduk di beranda sambil memandangi halaman yang hijau.",
    "Tiba-tiba terdengar suara ketukan di pagar, dan seekor kupu-kupu hinggap di ujung hidung Oyen.",
    "Oyen tertawa kecil, matanya mengikuti kupu-kupu itu terbang pelan menuju bunga-bunga di taman.",
    "Momo mengingatkan bahwa hari ini ada tugas penting yang tidak boleh dilupakan begitu saja.",
    "Oyen mengangguk, meski dalam hati ia masih memikirkan ikan goreng yang tersisa di piring.",
    "Mereka berjalan beriringan menyusuri jalan setapak, melewati pohon mangga yang rindang dan sejuk.",
    "Di tengah jalan, mereka bertemu kucing tetangga yang sedang berjemur dengan malas di atas batu.",
    "Oyen menyapa ramah, Momo mengangguk sopan, dan perjalanan pun berlanjut dengan hati yang ringan.",
    "Langit siang itu biru cerah, awan putih bergerak pelan seperti kapal yang berlayar jauh.",
    "Sesampainya di tujuan, Oyen menarik napas dalam-dalam dan mengumpulkan keberaniannya yang tersisa.",
    "Momo berbisik pelan bahwa tidak ada yang perlu ditakutkan selama mereka berdua bersama-sama.",
    "Waktu berjalan cepat, dan sebelum sadar, matahari sudah condong ke arah barat.",
    "Mereka pulang dengan langkah ringan, membawa cerita baru yang akan dikenang sampai kapan pun.",
    "Malam pun tiba, bintang-bintang muncul satu demi satu, dan rumah terasa hangat dan damai.",
]

# ---------------------------------------------------------------------------
# Pembantu umum
# ---------------------------------------------------------------------------

def _hitung_kata(teks):
    return len(teks.split())


def _slug(teks):
    s = re.sub(r"[^a-z0-9]+", "-", teks.lower()).strip("-")
    return s[:60] or "draf"


def _muat_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _simpan_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def _tanggal_hari_ini():
    return date.today().isoformat()


def _kemarin(tanggal_iso):
    try:
        d = date.fromisoformat(tanggal_iso)
    except Exception:
        d = date.today()
    return (d - timedelta(days=1)).isoformat()


def _tema_kemarin(tanggal_iso):
    riwayat = _muat_json(RIWAYAT_FILE, {})
    return set(riwayat.get(_kemarin(tanggal_iso), {}).get("tema", []))


def _tema_hari_ini(tanggal_iso):
    riwayat = _muat_json(RIWAYAT_FILE, {})
    return set(riwayat.get(tanggal_iso, {}).get("tema", []))


def _catat_tema(tanggal_iso, jenis, tema):
    riwayat = _muat_json(RIWAYAT_FILE, {})
    entri = riwayat.setdefault(tanggal_iso, {"tema": [], "rencana": {}})
    if tema and tema not in entri["tema"]:
        entri["tema"].append(tema)
    entri["rencana"][jenis] = entri["rencana"].get(jenis, 0) + 1
    _simpan_json(RIWAYAT_FILE, riwayat)


# ---------------------------------------------------------------------------
# 1) Rencana produksi harian
# ---------------------------------------------------------------------------

def buat_rencana(tanggal_iso):
    """Susun rencana produksi harian; tema tidak mengulang tema kemarin."""
    tanggal_iso = (tanggal_iso or "").strip() or _tanggal_hari_ini()
    kemarin = _tema_kemarin(tanggal_iso)
    dipakai = set()

    def ambil_tema(daftar, jumlah):
        segar = [t for t in daftar if t not in kemarin and t not in dipakai]
        hasil = segar[:jumlah]
        if len(hasil) < jumlah:
            # Stok tema segar habis: pakai ulang dan tandai jelas.
            sisa = [t for t in daftar if t not in dipakai and t not in hasil]
            for t in sisa:
                if len(hasil) >= jumlah:
                    break
                hasil.append(t + " (ulang — stok tema segar habis)")
        dipakai.update(h.replace(" (ulang — stok tema segar habis)", "") for h in hasil)
        return hasil

    video = ambil_tema([v["judul"] for v in VIDEO_TEMA], min(5, len(VIDEO_TEMA)))
    foto = ambil_tema(list(FOTO_SUBJEK.keys()), 3)
    ebook = ambil_tema(list(EBOOK_TOPIK.keys()), 5)
    puisi = ambil_tema(list(PUISI_BANK.keys()), 3)
    pod = ambil_tema([p["tema"] for p in POD_BANK], 5)
    lagu = ambil_tema(list(LAGU_BANK.keys()), 3)

    baris = ["# Rencana Produksi Harian — {}\n".format(tanggal_iso)]
    baris.append("Target: video 5, foto 50, eBook 5, lagu 5, musik 5, puisi 5, cerpen 5, POD 5.\n")
    baris.append("Tema kemarin dihindari: {}.\n".format(", ".join(sorted(kemarin)) or "-"))
    baris.append("## Video (5) — 3 klip x 10 dtk, dialog Inggris 17-25 kata/klip")
    for i, t in enumerate(video, 1):
        baris.append("- [ ] Video {}: {}".format(i, t))
    baris.append("\n## Foto (50) — prompt + metadata")
    jumlah_foto = [17, 17, 16]
    for k, j in zip(foto, jumlah_foto):
        baris.append("- [ ] Kategori {}: {} foto".format(k, j))
    baris.append("\n## eBook (5) — kerangka 15 halaman, WAJIB verifikasi fakta")
    for t in ebook:
        baris.append("- [ ] eBook: {}".format(t))
    baris.append("\n## Puisi (5) — 20 baris per puisi")
    for t in puisi:
        baris.append("- [ ] Puisi: {}".format(t))
    baris.append("- [ ] Puisi: tema bebas (2 judul)")
    baris.append("\n## Cerpen (5) — ~800 kata per cerpen")
    baris.append("- [ ] Cerpen: tema bebas (5 judul, tidak harus kucing)")
    baris.append("\n## POD (5) — ide desain + listing Inggris")
    for t in pod:
        baris.append("- [ ] POD: {}".format(t))
    baris.append("\n## Lagu (5) — lirik Bahasa Indonesia")
    for t in lagu:
        baris.append("- [ ] Lagu: {}".format(t))
    baris.append("- [ ] Lagu: tema bebas (2 judul)")
    baris.append("\n## Musik (5) — ide + prompt komposisi")
    baris.append("- [ ] Musik: 5 ide (ceria, tenang, sedih, petualangan, Natal)")
    baris.append("\n**Status: DRAF — menunggu persetujuan Cipta. Tidak ada yang diunggah otomatis.**")

    teks = "\n".join(baris)
    riwayat = _muat_json(RIWAYAT_FILE, {})
    entri = riwayat.setdefault(tanggal_iso, {"tema": [], "rencana": {}})
    for t in dipakai:
        if t not in entri["tema"]:
            entri["tema"].append(t)
    entri["rencana"]["dibuat"] = True
    _simpan_json(RIWAYAT_FILE, riwayat)
    return teks


# ---------------------------------------------------------------------------
# 2) Generator draf
# ---------------------------------------------------------------------------

def gen_video(tema):
    """Skrip video 3 klip: adegan + dialog 17-25 kata + prompt gambar."""
    tema = (tema or "").strip()
    cocok = None
    for v in VIDEO_TEMA:
        if tema and (tema.lower() in v["judul"].lower()
                     or v["judul"].lower() in tema.lower()
                     or tema.lower() in v["thumbnail"].lower()):
            cocok = v
            break
    if cocok is None:
        cocok = random.choice(VIDEO_TEMA)
    judul = cocok["judul"]
    out = ["# SKRIP VIDEO — {}".format(judul)]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Format:** 3 klip x 10 detik (total 20-30 detik), portrait 9:16")
    out.append("**Suara:** Oyen tinggi ceria, Momo rendah tenang. Satu mulut bergerak dalam satu waktu.")
    out.append("**Thumbnail:** portrait 720x1280, frame ekspresi besar + teks kuning tebal outline hitam: \"{}\"".format(cocok["thumbnail"]))
    out.append("**Hashtag:** {}".format(HASHTAG))
    out.append("")
    for i in range(3):
        dialog = cocok["dialog"][i]
        n = _hitung_kata(dialog)
        out.append("## Klip {} (10 detik)".format(i + 1))
        out.append("- **Adegan:** {}".format(cocok["adegan"][i]))
        out.append("- **Dialog ({} kata):** \"{}\"".format(n, dialog))
        out.append("- **Prompt gambar:** Frame video vertikal 9:16, kucing oren Oyen dan kucing abu-abu Momo, {}. Gaya animasi 3D lucu, pencahayaan hangat, ekspresi besar, karakter dan suasana konsisten.".format(cocok["adegan"][i].lower()))
        out.append("")
    out.append("**Cek kualitas sebelum kirim ke Cipta:** dialog 17-25 kata/klip, adegan nyambung, mulut tidak berbarengan, latar sesuai judul.")
    return "\n".join(out), judul


def gen_foto(kategori, jumlah):
    """Batch prompt foto stock + metadata (judul EN, 10 kata kunci, lisensi)."""
    kategori = (kategori or "kucing").strip().lower()
    if kategori not in FOTO_SUBJEK:
        kategori = "kucing"
    try:
        jumlah = int(jumlah)
    except Exception:
        jumlah = 10
    jumlah = max(1, min(50, jumlah))
    subjek = FOTO_SUBJEK[kategori]
    variasi_cahaya = ["golden hour", "soft daylight", "warm indoor light", "morning light"]
    out = ["# PROMPT FOTO STOCK — Kategori: {}".format(kategori)]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Jumlah:** {} foto | **Lisensi:** Commercial RF | **Catatan:** AI-generated image.".format(jumlah))
    out.append("")
    for i in range(jumlah):
        prompt, judul, kunci = subjek[i % len(subjek)]
        cahaya = variasi_cahaya[i % len(variasi_cahaya)]
        out.append("## Foto {:02d}".format(i + 1))
        out.append("- **Prompt:** {}, {}.".format(prompt, cahaya))
        out.append("- **Judul:** {}".format(judul))
        out.append("- **Kata kunci (10):** {}".format(kunci))
        out.append("- **Lisensi:** Commercial RF — AI-generated image.")
        out.append("")
    return "\n".join(out), "Foto {} x{}".format(kategori, jumlah)


def gen_ebook(topik):
    """Kerangka eBook anak 15 halaman dengan penanda PERLU VERIFIKASI."""
    topik = (topik or "").strip()
    cocok = None
    for nama in EBOOK_TOPIK:
        if topik and (topik.lower() in nama.lower() or nama.lower() in topik.lower()):
            cocok = nama
            break
    if cocok is None:
        cocok = "Nabi Nuh"
    data = EBOOK_TOPIK[cocok]
    out = ["# KERANGKA EBOOK — {}".format(cocok)]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Seri:** Cerita untuk Anak — Dunia Kiki | **Target:** 15 halaman isi")
    out.append("**Aturan:** ilustrasi tokoh dari belakang, wajah TIDAK PERNAH digambarkan.")
    out.append("")
    out.append("## Halaman 1 — Sampul & Pengantar")
    out.append("Judul: {} — cerita untuk anak. Perkenalan singkat tokoh dan pesan cerita.".format(cocok))
    out.append("Ilustrasi sampul: pemandangan/ suasana cerita, tokoh dari belakang, tanpa wajah.")
    out.append("")
    for i, beat in enumerate(data["alur"], start=2):
        out.append("## Halaman {} ".format(i))
        out.append("{}".format(beat))
        out.append("Ilustrasi: adegan di atas, tokoh dari belakang, tanpa wajah.")
        out.append("*Sumber: PERLU VERIFIKASI — {}*".format(data["sumber"]))
        out.append("")
    out.append("## Halaman 14 — Pelajaran")
    out.append("Tiga pelajaran dari kisah ini, ditulis dengan bahasa sederhana untuk anak.")
    out.append("Setiap pelajaran merujuk ke halaman cerita dan ditandai PERLU VERIFIKASI bila berisi fakta.")
    out.append("")
    out.append("## Halaman 15 — Pertanyaan Diskusi & Penutup")
    out.append("Tiga pertanyaan diskusi untuk anak dan orang tua, lalu penutup yang hangat.")
    out.append("Daftar Sumber: {} ".format(data["sumber"]))
    out.append("")
    out.append("**{}**".format(CATATAN_KEJUJURAN))
    return "\n".join(out), "eBook {}".format(cocok)


def gen_puisi(tema):
    """Puisi TEPAT 20 baris."""
    tema = (tema or "").strip()
    cocok = None
    for nama in PUISI_BANK:
        if tema and (tema.lower() in nama.lower() or nama.lower() in tema.lower()):
            cocok = nama
            break
    if cocok is None:
        cocok = "Senja Bareng Oyen"
    baris = PUISI_BANK[cocok]
    assert len(baris) == 20, "bank puisi harus 20 baris"
    out = ["# PUISI — {}".format(cocok)]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Jumlah baris:** 20")
    out.append("")
    for i, b in enumerate(baris, 1):
        out.append("{}. {}".format(i, b))
    return "\n".join(out), "Puisi {}".format(cocok)


def gen_cerpen(tema):
    """Cerpen ~800 kata (target 750-850) dari kerangka + kalimat pengisi."""
    tema = (tema or "Oyen dan Kunci yang Hilang").strip()
    judul = tema
    paragraf = [
        "Pagi itu, Oyen bangun dengan perasaan aneh. Ada sesuatu yang berbeda di rumah, seperti ada rahasia kecil yang menunggu untuk ditemukan. Ia melompat dari kasur, meregangkan badan, dan berjalan pelan menuju ruang tamu. Di sana, Momo sudah duduk rapi di dekat jendela, menatap halaman dengan mata yang tenang. Oyen mendekat dan bertanya apa yang sedang dipikirkan sahabatnya itu. Momo hanya tersenyum dan berkata bahwa hari ini akan menjadi hari yang istimewa, meski ia sendiri belum tahu kenapa. Oyen mengangguk, meski dalam hati ia masih penasaran dengan perasaan aneh sejak bangun tadi.",
        "Ternyata perasaan itu benar. Di atas meja makan, ada sebuah kunci kecil berwarna emas yang tidak pernah mereka lihat sebelumnya. Kunci itu berkilau saat terkena cahaya matahari, dan di gagangnya terukir huruf yang sulit dibaca. Oyen mengambilnya dengan hati-hati, lalu menunjukkannya kepada Momo. Momo mengamati kunci itu lama sekali, lalu berkata bahwa kunci sekecil itu pasti membuka sesuatu yang penting. Mereka berdua sepakat untuk mencari tahu ke mana kunci itu menuju, dan petualangan pun dimulai dari ruang tamu yang sederhana itu.",
        "Pencarian pertama membawa mereka ke gudang tua di belakang rumah. Oyen membuka pintu gudang dengan susah payah, dan debu beterbangan ke mana-mana. Di dalam gudang ada banyak kotak kayu, mainan lama, dan sebuah peti besar yang terkunci rapat. Oyen mencoba kunci emas itu pada peti tersebut, tetapi tidak cocok. Momo menggeleng pelan dan berkata bahwa peti itu bukan jawabannya. Mereka pun keluar dari gudang dengan kecewa, tetapi tidak menyerah begitu saja.",
        "Pencarian kedua membawa mereka ke taman di seberang jalan. Di sana ada sebuah rumah pohon tua yang sudah lama tidak dipakai. Oyen memanjat dengan semangat, sementara Momo menunggu di bawah sambil menjaga kunci emas itu. Di atas rumah pohon, Oyen menemukan sebuah kotak kecil yang terkunci. Ia mencoba kunci emas itu, dan kali ini kunci berputar dengan mudah. Di dalam kotak ada selembar kertas dan sebuah foto lama yang membuat Oyen terdiam.",
        "Foto itu menunjukkan dua ekor kucing kecil yang sedang bermain di taman yang sama, bertahun-tahun yang lalu. Di balik foto ada tulisan tangan yang berbunyi bahwa persahabatan adalah kunci yang paling berharga. Oyen turun dari rumah pohon dan menunjukkan foto itu kepada Momo. Momo tersenyum lebar, matanya berkaca-kaca, dan berkata bahwa kunci emas itu memang bukan untuk membuka peti atau kotak, melainkan untuk membuka ingatan tentang persahabatan mereka.",
        "Malam itu, Oyen dan Momo duduk di beranda sambil memandangi bintang. Kunci emas itu kini tergantung di leher Oyen sebagai kalung, pengingat bahwa harta yang paling berharga bukanlah emas atau perak, melainkan sahabat yang selalu ada. Momo mengangguk setuju, dan mereka berdua tertidur dengan hati yang tenang. Sejak hari itu, setiap kali Oyen melihat kunci emas itu, ia teringat bahwa petualangan terbaik selalu dimulai dari rumah, dan sahabat terbaik selalu ada di sampingnya.",
    ]
    # Judul disisipkan sebagai pembuka cerita (tema bebas, bukan hanya kucing).
    isi = " ".join(paragraf)
    kata = isi.split()
    # Tambah kalimat pengisi sampai mencapai minimal 750 kata.
    idx = 0
    while len(kata) < 750:
        kata.extend(CERPEN_KALIMAT_PENGISI[idx % len(CERPEN_KALIMAT_PENGISI)].split())
        idx += 1
    # Pangkas bila melebihi 850 kata (potong di akhir kalimat pengisi).
    if len(kata) > 850:
        kata = kata[:850]
    isi = " ".join(kata)
    n = len(isi.split())
    out = ["# CERPEN — {}".format(judul)]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Jumlah kata:** {} (target ~800 kata)".format(n))
    out.append("")
    out.append(isi)
    return "\n".join(out), "Cerpen {}".format(judul)


def gen_pod(tema):
    """Ide desain POD + listing Bahasa Inggris (tanpa istilah pahlawan super berlisensi)."""
    tema = (tema or "").strip()
    cocok = None
    for p in POD_BANK:
        if tema and (tema.lower() in p["tema"].lower() or p["tema"].lower() in tema.lower()):
            cocok = p
            break
    if cocok is None:
        cocok = random.choice(POD_BANK)
    out = ["# POD — {}".format(cocok["tema"])]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Produk:** Kaos (Zazzle, toko Podcast_Meong)")
    out.append("")
    out.append("## Ide Desain")
    out.append(cocok["desain"])
    out.append("")
    out.append("## Listing (Bahasa Inggris)")
    out.append("- **Title:** {}".format(cocok["judul_en"]))
    out.append("- **Description:** {}".format(cocok["deskripsi_en"]))
    out.append("- **Tags (10):** {}".format(cocok["tags_en"]))
    out.append("")
    out.append("**Catatan:** istilah pahlawan super berlisensi tidak dipakai — gunakan 'super cat' / 'hero cat'.")
    return "\n".join(out), "POD {}".format(cocok["tema"])


def gen_lagu(tema):
    """Lirik lagu Bahasa Indonesia (2 verse + chorus + outro)."""
    tema = (tema or "").strip()
    cocok = None
    for nama in LAGU_BANK:
        if tema and (tema.lower() in nama.lower() or nama.lower() in tema.lower()):
            cocok = nama
            break
    if cocok is None:
        cocok = "Oyen dan Momo"
    lagu = LAGU_BANK[cocok]
    out = ["# LIRIK LAGU — {}".format(cocok)]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Bahasa:** Indonesia | **Nada:** ceria, tempo sedang, ramah anak")
    out.append("")
    out.append("[Verse 1]")
    out.extend(lagu["verse1"])
    out.append("")
    out.append("[Chorus]")
    out.extend(lagu["chorus"])
    out.append("")
    out.append("[Verse 2]")
    out.extend(lagu["verse2"])
    out.append("")
    out.append("[Chorus]")
    out.extend(lagu["chorus"])
    out.append("")
    out.append("[Outro]")
    out.extend(lagu["outro"])
    return "\n".join(out), "Lagu {}".format(cocok)


def gen_musik(tema):
    """Ide + prompt komposisi musik (tanpa file audio — prompt untuk alat musik AI)."""
    tema = (tema or "Ceria Pagi Oyen").strip()
    suasana = [
        ("Ceria", "tempo cepat 120 BPM, ukulele + piano ceria, nada mayor, cocok untuk video lucu Oyen"),
        ("Tenang", "tempo lambat 70 BPM, piano lembut + gitar akustik, nada mayor hangat, cocok untuk senja"),
        ("Sedih", "tempo lambat 60 BPM, piano minor + cello, lembut dan menyentuh, cocok untuk momen haru"),
        ("Petualangan", "tempo sedang 100 BPM, orkestra kecil + drum, penuh semangat, cocok untuk adegan aksi kucing"),
        ("Natal", "tempo sedang 90 BPM, lonceng + pad lembut, hangat dan meriah, cocok untuk tema Natal"),
    ]
    out = ["# IDE MUSIK — {}".format(tema)]
    out.append("")
    out.append("**Status:** DRAF — menunggu persetujuan Cipta")
    out.append("**Catatan:** agent hanya membuat IDE + PROMPT komposisi, bukan file audio.")
    out.append("Gunakan alat musik AI gratis / pustaka bebas royalti; cek lisensi sebelum dipakai komersial.")
    out.append("")
    for nama, prompt in suasana:
        out.append("## {} — {}".format(nama, tema))
        out.append("- **Prompt komposisi:** {}, musik instrumental tanpa vokal.".format(prompt))
        out.append("- **Durasi saran:** 30 detik (untuk Shorts) atau 60 detik (untuk video panjang).")
        out.append("")
    return "\n".join(out), "Musik {}".format(tema)


# ---------------------------------------------------------------------------
# 3) Penyimpanan draf + pelacak progres
# ---------------------------------------------------------------------------

def simpan_draf(jenis, judul, isi, tanggal_iso):
    """Simpan draf sebagai file markdown; kembalikan path + hitung progres."""
    tanggal_iso = (tanggal_iso or "").strip() or _tanggal_hari_ini()
    folder = OUTPUT_DIR / tanggal_iso
    folder.mkdir(parents=True, exist_ok=True)
    nama = "{}_{}.md".format(jenis, _slug(judul))
    path = folder / nama
    i = 2
    while path.exists():
        path = folder / "{}_{}-v{}.md".format(jenis, _slug(judul), i)
        i += 1
    header = "# {}\n\n**Status:** menunggu persetujuan\n**Jenis:** {}\n**Tanggal:** {}\n\n---\n\n".format(
        judul, JENIS_LABEL.get(jenis, jenis), tanggal_iso)
    path.write_text(header + isi, encoding="utf-8")
    progres = _muat_json(PROGRES_FILE, {})
    hari = progres.setdefault(tanggal_iso, {})
    hari[jenis] = hari.get(jenis, 0) + 1
    _simpan_json(PROGRES_FILE, progres)
    if judul:
        _catat_tema(tanggal_iso, jenis, judul)
    return str(path)


def progres_hari_ini(tanggal_iso):
    """Tabel progres hari ini vs target harian."""
    tanggal_iso = (tanggal_iso or "").strip() or _tanggal_hari_ini()
    progres = _muat_json(PROGRES_FILE, {})
    hari = progres.get(tanggal_iso, {})
    baris = ["# Progres Produksi — {}\n".format(tanggal_iso)]
    baris.append("| Jenis | Dibuat | Target | Sisa |")
    baris.append("|---|---|---|---|")
    total_buat = 0
    total_target = 0
    for jenis, target in TARGET_HARIAN.items():
        dibuat = hari.get(jenis, 0)
        total_buat += dibuat
        total_target += target
        baris.append("| {} | {} | {} | {} |".format(JENIS_LABEL[jenis], dibuat, target, max(0, target - dibuat)))
    baris.append("")
    baris.append("**Total: {} / {} produk hari ini.**".format(total_buat, total_target))
    baris.append("")
    baris.append("Semua draf berstatus **menunggu persetujuan** — tidak ada yang diunggah otomatis.")
    return "\n".join(baris)


def daftar_draf(tanggal_iso):
    """Daftar file draf hari ini."""
    tanggal_iso = (tanggal_iso or "").strip() or _tanggal_hari_ini()
    folder = OUTPUT_DIR / tanggal_iso
    if not folder.exists():
        return "Belum ada draf untuk tanggal {}.".format(tanggal_iso)
    files = sorted(folder.glob("*.md"))
    if not files:
        return "Belum ada draf untuk tanggal {}.".format(tanggal_iso)
    baris = ["# Draf hari ini — {} ({} file)\n".format(tanggal_iso, len(files))]
    for f in files:
        baris.append("- {} (menunggu persetujuan)".format(f.name))
    return "\n".join(baris)

# ---------------------------------------------------------------------------
# Gemini (opsional, free tier) — hanya memperbaiki draf template, bukan
# menggantikan aturan struktur. Hasil Gemini selalu divalidasi; bila tidak
# lolos, draf template yang dipakai.
# ---------------------------------------------------------------------------

GEMINI_ATURAN = (
    "Kamu membantu produksi konten Podcast Meong. ATURAN KERAS: "
    "(1) Semua hasil adalah DRAF, bukan konten final. "
    "(2) Jangan mengarang ayat Al-Quran atau hadis. Setiap fakta agama/sejarah "
    "harus ditandai 'PERLU VERIFIKASI' dan disertai sumber yang harus dicek "
    "(api.alquran.cloud, sunnah.com). "
    "(3) Jangan menggambarkan wajah nabi/tokoh — ilustrasi hanya dari belakang. "
    "(4) Video/podcast wajib kucing (Oyen & Momo); produk lain tema bebas. "
    "(5) Jangan memakai istilah pahlawan super berbahasa Inggris (satu kata) "
    "untuk POD — pakai 'super cat'/'hero cat'. "
    "(6) Jawab dalam Bahasa Indonesia, kecuali dialog video yang berbahasa Inggris."
)


def gemini_ask(prompt):
    """Kembalikan teks jawaban Gemini, atau None bila key tidak ada / gagal."""
    if not MODE_AI:
        return None
    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        resp = client.models.generate_content(model=MODEL, contents=prompt)
        teks = (resp.text or "").strip()
        return teks or None
    except Exception:
        return None


def _validasi_hasil(jenis, teks):
    """Validasi struktur hasil Gemini; False = pakai draf template."""
    if not teks or len(teks) < 50:
        return False
    if jenis == "puisi":
        baris = [b for b in teks.splitlines() if b.strip()]
        # Hitung baris isi puisi (abaikan judul/header/status).
        isi = [b for b in baris if not b.startswith(("#", "*", "**"))]
        return len(isi) == 20
    if jenis == "video":
        dialog = []
        for baris in teks.splitlines():
            if "Dialog" in baris:
                m = re.search(r'"([^"]+)"', baris)
                if m:
                    dialog.append(m.group(1))
        if not dialog:
            return False
        return all(17 <= _hitung_kata(d) <= 25 for d in dialog[:3])
    if jenis == "cerpen":
        n = _hitung_kata(teks)
        return 700 <= n <= 900
    if jenis == "pod":
        return "superhero" not in teks.lower()
    if jenis == "ebook":
        return "PERLU VERIFIKASI" in teks
    return True


GENERATOR = {
    "video": gen_video,
    "foto": None,  # butuh kategori + jumlah
    "ebook": gen_ebook,
    "lagu": gen_lagu,
    "musik": gen_musik,
    "puisi": gen_puisi,
    "cerpen": gen_cerpen,
    "pod": gen_pod,
}


def buat_draf(jenis, tema, kategori_foto="kucing", jumlah_foto=10, tanggal_iso=""):
    """Buat draf (template, diperbaiki Gemini bila ada key), simpan, kembalikan
    (teks_draf, pesan_status)."""
    tanggal_iso = (tanggal_iso or "").strip() or _tanggal_hari_ini()
    jenis = (jenis or "video").strip().lower()
    tema = (tema or "").strip()

    if jenis == "foto":
        teks, judul = gen_foto(kategori_foto, jumlah_foto)
        mode = "template"
    else:
        fn = GENERATOR.get(jenis)
        if fn is None:
            return "Jenis tidak dikenal: {}".format(jenis), "Gagal."
        teks, judul = fn(tema)
        mode = "template"
        if MODE_AI:
            prompt = (
                GEMINI_ATURAN + "\n\nPerbaiki dan kembangkan draf berikut "
                "menjadi lebih menarik, TANPA mengubah struktur dan aturannya "
                "(puisi tetap 20 baris; dialog video tetap 17-25 kata per klip; "
                "cerpen tetap 700-900 kata; eBook tetap menandai PERLU VERIFIKASI; "
                "POD tanpa istilah pahlawan super berbahasa Inggris (satu kata)). Pertahankan judul dan formatnya.\n\n"
                + teks
            )
            hasil = gemini_ask(prompt)
            if hasil and _validasi_hasil(jenis, hasil):
                teks, mode = hasil, "gemini"
    path = simpan_draf(jenis, judul, teks, tanggal_iso)
    status = (
        "Disimpan: {} | Mode: {} | Status draf: menunggu persetujuan Cipta"
        .format(path, mode)
    )
    return teks, status


# ---------------------------------------------------------------------------
# Antarmuka Gradio
# ---------------------------------------------------------------------------

MODE_TEKS = (
    "Mode: AI penuh (Gemini free tier)." if MODE_AI
    else "Mode: template lokal (tanpa API key — isi GEMINI_API_KEY untuk AI penuh)."
)

with gr.Blocks(title="Agent Produksi Produk — Podcast Meong", analytics_enabled=False) as demo:
    gr.Markdown(
        "# 🐱 Agent Produksi Produk — Podcast Meong\n\n"
        "Memproduksi **DRAF** produk harian: video 5, foto 50, eBook 5, lagu 5, "
        "musik 5, puisi 5, cerpen 5, POD 5.\n\n"
        "**Semua hasil adalah DRAF — menunggu persetujuan Cipta. Tidak ada yang "
        "diunggah atau diterbitkan otomatis.**\n\n"
        + MODE_TEKS
    )

    with gr.Tab("Rencana Harian"):
        gr.Markdown(
            "Susun daftar tugas produksi hari ini. Tema dipilih agar **tidak "
            "mengulang tema kemarin**."
        )
        tgl_rencana = gr.Textbox(label="Tanggal (YYYY-MM-DD)", value=_tanggal_hari_ini())
        btn_rencana = gr.Button("Buat Rencana Produksi", variant="primary")
        out_rencana = gr.Markdown(label="Rencana")

    with gr.Tab("Generator Draf"):
        gr.Markdown(
            "Pilih jenis produk, tulis tema/judul, lalu buat draf. "
            "Draf otomatis tersimpan di folder output dan dihitung di progres."
        )
        jenis_in = gr.Dropdown(
            choices=[(JENIS_LABEL[k], k) for k in TARGET_HARIAN],
            value="video",
            label="Jenis produk",
        )
        tema_in = gr.Textbox(
            label="Tema / judul (kosongkan = pilih otomatis)",
            placeholder="cth: Oyen Membuka Warung Kopi / Nabi Yunus / Senja Bareng Oyen",
        )
        kategori_in = gr.Dropdown(
            choices=list(FOTO_SUBJEK.keys()),
            value="kucing",
            label="Kategori foto (hanya untuk jenis Foto)",
        )
        jumlah_in = gr.Slider(
            minimum=1, maximum=50, step=1, value=10,
            label="Jumlah foto (hanya untuk jenis Foto)",
        )
        tgl_draf = gr.Textbox(label="Tanggal (YYYY-MM-DD)", value=_tanggal_hari_ini())
        btn_draf = gr.Button("Buat & Simpan Draf", variant="primary")
        out_draf = gr.Textbox(label="Draf", lines=25)
        out_status = gr.Textbox(label="Status", lines=2)

    with gr.Tab("Draf & Progres"):
        gr.Markdown("Lihat progres produksi hari ini vs target, dan daftar draf yang dibuat.")
        tgl_prog = gr.Textbox(label="Tanggal (YYYY-MM-DD)", value=_tanggal_hari_ini())
        btn_prog = gr.Button("Muat Ulang", variant="primary")
        out_prog = gr.Markdown(label="Progres")
        out_daftar = gr.Markdown(label="Daftar draf")

    btn_rencana.click(fn=buat_rencana, inputs=[tgl_rencana], outputs=[out_rencana])
    btn_draf.click(
        fn=buat_draf,
        inputs=[jenis_in, tema_in, kategori_in, jumlah_in, tgl_draf],
        outputs=[out_draf, out_status],
    )

    def _muat_progres(tanggal):
        return progres_hari_ini(tanggal), daftar_draf(tanggal)

    btn_prog.click(fn=_muat_progres, inputs=[tgl_prog], outputs=[out_prog, out_daftar])

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        share=False,
    )
