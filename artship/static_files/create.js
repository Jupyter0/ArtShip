document.addEventListener("DOMContentLoaded", () => {
    const updateText = (inputId, previewId) => {
      const input = document.getElementById(inputId);
      if (input) {
        input.addEventListener("input", () => {
          document.getElementById(previewId).textContent = input.value || `[${previewId.replace('preview-', '').replace(/-/g, ' ')}]`;
        });
      }
    };

    updateText("id_pieceName", "preview-title");
    updateText("id_artistName", "preview-artist");
    updateText("id_condition", "preview-condition");
    updateText("id_description", "preview-description");
    updateText("id_startingBid", "preview-starting");
    updateText("id_priceBIN", "preview-bin");

    const imageInput = document.getElementById("id_preview");
    if (imageInput) {
      imageInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (event) {
            const img = document.getElementById("preview-image");
            img.src = event.target.result;
            img.style.display = "block";
          };
          reader.readAsDataURL(file);
        }
      });
    }
  });