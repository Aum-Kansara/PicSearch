const fileInput = document.querySelector(".file"),
previewImg = document.querySelector(".preview-img img")
const loadImage = () => {
    let file = fileInput.files[0];
    if(!file) return;
    previewImg.src = URL.createObjectURL(file);
    previewImg.addEventListener("load", () => {
        resetFilterBtn.click();
        document.querySelector(".preview-img").classList.remove("disable");
    });
}
fileInput.addEventListener("change", loadImage);