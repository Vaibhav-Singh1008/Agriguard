const uploadBox = document.querySelector('.upload-box');
const fileInput = document.querySelector('#file-input');
const boxText = document.querySelector('.upload-box span');

uploadBox.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (event) => {
    if(event.target.files.length > 0) {
        const fileName = event.target.files[0].name;
        boxText.textContent = fileName;
        uploadBox.style.backgroundColor = "#c8e6c9";
        uploadBox.style.border = "2px solid #1b5e20";
    }
});

const aiBtn = document.querySelector('#ai-btn');
const aiResponse = document.querySelector('#ai-response');
const aiText = document.querySelector('#ai-text');
const prevCrop = document.querySelector('#prev-crop');
const soilType = document.querySelector('#soil-type');
const langSelect = document.querySelector('#lang-select');

aiBtn.addEventListener('click', () => {
    let crop = prevCrop.value.trim().toLowerCase();
    let soil = soilType.value;
    let lang = langSelect ? langSelect.value : "en"; 
    let advice = "";

    if (crop === "") {
        if (lang === "hi") {
            alert("कृपया पहले पिछली फसल का नाम लिखें!");
        } else {
            alert("Please enter the previous crop name first!");
        }
        return;
    }

    if (crop === "wheat" || crop === "gehun") {
        if (lang === "hi") {
            advice = "गेहूँ मिट्टी से बहुत सारा नाइट्रोजन सोख लेता है। मिट्टी की ताकत वापस लाने के लिए अगली बार दलहन (चना या दाल) उगाएं और जैविक खाद डालें।";
        } else {
            advice = "Wheat absorbs a lot of nitrogen. Plant Legumes (Chana/Dal) next to naturally restore soil fertility. Add organic compost.";
        }
    } else if (crop === "sugarcane" || crop === "ganna") {
        if (lang === "hi") {
            advice = "गन्ना मिट्टी के पोषक तत्व और पानी बहुत खींचता है। इसके बाद सरसों या आलू उगाएं। सही मात्रा में NPK खाद का प्रयोग करें।";
        } else {
            advice = "Sugarcane drains heavy nutrients and water. Rotate with Mustard or Potatoes. Use balanced NPK fertilizers.";
        }
    } else if (crop === "rice" || crop === "dhan") {
        if (lang === "hi") {
            advice = "धान की खेती से मिट्टी सख्त हो जाती है। अगली फसल बोने से पहले गहरी जुताई करें और हरी खाद वाली फसलें उगाएं।";
        } else {
            advice = "Rice farming compacts the soil. Plough deep and grow Green Manure crops before the next planting.";
        }
    } else {
        if (lang === "hi") {
            advice = "फसल चक्र (Crop Rotation) का ध्यान रखें। मिट्टी की सेहत और पैदावार बढ़ाने के लिए गोबर की खाद का प्रयोग करें।";
        } else {
            advice = "Ensure proper crop rotation. Add cow dung manure (Gobar Khad) to improve overall soil health and yield.";
        }
    }

    if (soil === "sandy") {
        if (lang === "hi") {
            advice += " रेतीली मिट्टी में पानी जल्दी नीचे चला जाता है, इसलिए ड्रिप इरीगेशन (बूंद-बूंद सिंचाई) का इस्तेमाल करें।";
        } else {
            advice += " For sandy soil, use drip irrigation as it loses water quickly.";
        }
    } else if (soil === "clay") {
        if (lang === "hi") {
            advice += " चिकनी मिट्टी में पानी ज्यादा भरता है। जड़ों को सड़ने से बचाने के लिए खेत में जलभराव न होने दें।";
        } else {
            advice += " Clay soil holds too much water. Ensure proper drainage to prevent root rot.";
        }
    }

    aiText.textContent = advice;
    aiResponse.style.display = "block";
});
