const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");

// Access camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing camera:", error);
    });

document.getElementById("captureButton").addEventListener("click", function() {
    context.drawImage(video, 0, 0, 640, 480);
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append("image", blob, "captured_image.png");
        const contactNumber = document.getElementById("contactNumber").value;
        formData.append("contactNumber", contactNumber);

        fetch("/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (response.status === 400) {
                return response.json().then(errorData => {
                    alert(errorData.error);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data && data.name) {
                document.getElementById("result").innerHTML = `
                    <p>Name: ${data.name}</p>
                    <p>Register Number: ${data.register_number}</p>
                    <p>Sign-in Time: ${data.sign_in_time}</p>
                `;
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }, "image/png");
});