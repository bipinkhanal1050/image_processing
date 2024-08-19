document.addEventListener("DOMContentLoaded", function () {
  const imageContainer = document.getElementById("image-container");
  const messageContainer = document.getElementById("message-container");
  const mainImage = document.getElementById("main-image");

  // Function to load and display image with invisible buttons
  function loadImage(imageIndex) {
    // Load the image
    mainImage.src = `images/${imageIndex}.png`;

    // Load the JSON data
    fetch(`purified/purified${imageIndex}.json`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((jsonData) => {
        // Clear previous buttons and text
        const elements = imageContainer.querySelectorAll(
          ".button, .button-text"
        );
        elements.forEach((element) => element.remove());

        // Create and place invisible buttons on the image
        jsonData.forEach((data) => {
          const button = document.createElement("button");
          button.className = "button";

          // Calculate button position and size
          const topLeft = data.top_left;
          const bottomRight = data.bottom_right;
          const width = bottomRight[0] - topLeft[0];
          const height = bottomRight[1] - topLeft[1];

          // Set button style
          button.style.position = "absolute";
          button.style.left = `${topLeft[0] - 5}px`;
          button.style.top = `${topLeft[1] - 5}px`;
          button.style.width = `${width + 10}px`;
          button.style.height = `${height + 10}px`;
          button.style.backgroundColor = "rgba(0, 128, 0, 0.2)";
          button.style.border = "none";
          button.style.borderRadius = "50%";
          button.style.padding = "5px";

          // Add click event to button
          button.addEventListener("click", function () {
            const message = `Button with value ${data.text} is clicked`;
            console.log(message);
            messageContainer.innerText = message; // Display message
          });

          // Append button to image container   
          imageContainer.appendChild(button);

          // Create and position text below the button
          const textElement = document.createElement("div");
          textElement.className = "button-text";
          textElement.innerText = data.text;
          textElement.style.left = `${topLeft[0] + width+4 }px`;
          textElement.style.top = `${topLeft[1] + height/2-1 }px`;
          textElement.style.color = "red";
          textElement.style.background = "none";
          textElement.style.fontSize = "12px";
          textElement.style.fontWeight = "bold";

          // Append text to image container
          imageContainer.appendChild(textElement);
        });
      })
      .catch((error) => {
        console.error("Error loading JSON:", error);
      });
  }

  // Load the initial image
  loadImage(1);

  // Expose loadImage to global scope
  window.loadImage = loadImage;
});
