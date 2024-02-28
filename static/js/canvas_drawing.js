
$("form").on('submit', function () {
    // disable button
    $("#submit-btn").prop("disabled", true);
    // add spinner to button
    $("#submit-btn").html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`
    );
})


let dataURL = ""
let signature = $("#id_signature").val();


if ($("#area_of_soreness").val()) {
    dataURL = $("#area_of_soreness").val()
}


// define canvas
const bodyCanvas = document.querySelector('.js-paint.body')
const bodyContext = bodyCanvas.getContext('2d')
bodyContext.lineCap = 'round';
bodyContext.lineWidth = 1;



const signatureCanvas = document.querySelector('.js-paint.signature')
const signatureContext = signatureCanvas.getContext('2d')
signatureContext.lineCap = 'round';
signatureContext.strokeStyle = '#000000';
signatureContext.lineWidth = 1;


let originalBodyImage = new Image();
originalBodyImage.src = '/static/img/body.png'
let bodyImage = new Image();

bodyImage.src = dataURL != "" ? dataURL : originalBodyImage.src;

bodyImage.onload = function () {
    bodyCanvas.width = bodyCanvas.offsetWidth
    bodyCanvas.height = bodyCanvas.offsetHeight
    bodyContext.drawImage(bodyImage, 0, 0, bodyCanvas.offsetWidth,bodyCanvas.offsetHeight);
}

addEventListener("resize", (event) => {
    bodyCanvas.width = bodyCanvas.offsetWidth
    bodyCanvas.height = bodyCanvas.offsetHeight
    bodyContext.clearRect(0, 0, bodyCanvas.offsetWidth, bodyCanvas.offsetHeight)
    let img = new Image()
    img.src = dataURL != "" ? dataURL : '/static/img/body.png';
    bodyContext.drawImage(img, 0, 0, bodyCanvas.offsetWidth, bodyCanvas.offsetHeight);

});

if (signature) {

    let signatureImage = new Image();
    signatureImage.src = signature

    signatureImage.onload = function () {
        signatureContext.drawImage(signatureImage, 0, 0, 600, 600)
    }

}

// initialize state 
let x = 0, y = 0;
let isMouseDown = false;
let isBack = false;
let isBody = false;
let isSignature = false;
let pointerAmount = []



const stopDrawing = () => {

    if (isMouseDown) {
        dataURL = bodyCanvas.toDataURL()
        isMouseDown = false;
        if (isBody) {
            $("#area_of_soreness").val(dataURL)
        } else if (isSignature) {
            $("#id_signature").val(signatureCanvas.toDataURL())
        }
        isBody = false;
        isSignature = false;
        pointerAmount = [];

    }
}

const startDrawing = event => {
    isMouseDown = true;
    [x, y] = [event.offsetX, event.offsetY];
}

const drawingBody = event => {
    pointerAmount.push(event)

    let eventAmount = 0
    for (let i = 0; i < pointerAmount.length; i++) {
        if (event instanceof PointerEvent) {
            eventAmount++
        }
    }

    bodyCanvas.style.touchAction = "None"
    isBody = true
}


const drawingSignature = event => {
    pointerAmount.push(event)

    let eventAmount = 0
    for (let i = 0; i < pointerAmount.length; i++) {
        if (event instanceof PointerEvent) {
            eventAmount++
        }
    }

    signatureCanvas.style.touchAction = "None"
    isSignature = true

}


const drawLine = event => {
    if (isMouseDown) {
        const newX = event.offsetX;
        const newY = event.offsetY;

        let context;

        if (isBody) {
            context = bodyContext
            context.strokeStyle = 'red';
        } else {
            context = signatureContext
        }

        context.beginPath();
        context.moveTo(x, y);
        context.lineTo(newX, newY);
        context.stroke();
        x = newX;
        y = newY;
    }
}


function clearBodyCanvas() {
    bodyCanvas.width = bodyCanvas.offsetWidth
    bodyCanvas.height = bodyCanvas.offsetHeight
    bodyContext.clearRect(0, 0, bodyCanvas.offsetWidth, bodyCanvas.offsetHeight)
    bodyContext.drawImage(originalBodyImage, 0, 0, bodyCanvas.offsetWidth, bodyCanvas.offsetHeight);

    dataURL = bodyCanvas.toDataURL()
    $("#area_of_soreness").val("")
}



function clearSignatureCanvas() {
    signatureContext.clearRect(0, 0, 300, 100)
    $("#id_signature").val("")
}


bodyCanvas.addEventListener('mousedown', startDrawing);
bodyCanvas.addEventListener('mousedown', drawingBody);
bodyCanvas.addEventListener('mousemove', drawLine);
bodyCanvas.addEventListener('mouseup', stopDrawing);
bodyCanvas.addEventListener('mouseout', stopDrawing);

signatureCanvas.addEventListener('mousedown', startDrawing);
signatureCanvas.addEventListener('mousedown', drawingSignature);
signatureCanvas.addEventListener('mousemove', drawLine);
signatureCanvas.addEventListener('mouseup', stopDrawing);
signatureCanvas.addEventListener('mouseout', stopDrawing);

bodyCanvas.addEventListener('pointerdown', startDrawing);
bodyCanvas.addEventListener('pointerdown', drawingBody);
bodyCanvas.addEventListener('pointermove', drawLine);
bodyCanvas.addEventListener('pointerup', stopDrawing);
bodyCanvas.addEventListener('pointerout', stopDrawing);


signatureCanvas.addEventListener('pointerdown', startDrawing);
signatureCanvas.addEventListener('pointerdown', drawingSignature);
signatureCanvas.addEventListener('pointermove', drawLine);
signatureCanvas.addEventListener('pointerup', stopDrawing);
signatureCanvas.addEventListener('pointerout', stopDrawing);
