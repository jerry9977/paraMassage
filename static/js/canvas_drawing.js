
$("form").on('submit', function () {
    // disable button
    $("#submit-btn").prop("disabled", true);
    // add spinner to button
    $("#submit-btn").html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`
    );
})


let frontBackCanvas = {
    frontDataUrl: "",
    backDataUrl: "",
}
let signature = $("#id_signature").val();


console.log($("#id_area_of_soreness_front").val())
if ($("#id_area_of_soreness_front").val()) {
    frontBackCanvas.frontDataUrl = $("#id_area_of_soreness_front").val()
}

if ($("#id_area_of_soreness_back").val()) {
    frontBackCanvas.backDataUrl = $("#id_area_of_soreness_back").val()
}

// define canvas
const frontCanvas = document.querySelector('.js-paint.front')
const frontContext = frontCanvas.getContext('2d')
frontContext.lineCap = 'round';
frontContext.strokeStyle = '#000000';
frontContext.lineWidth = 1;

const backCanvas = document.querySelector('.js-paint.back')
const backContext = backCanvas.getContext('2d')
backContext.lineCap = 'round';
backContext.strokeStyle = '#000000';
backContext.lineWidth = 1;


const signatureCanvas = document.querySelector('.js-paint.signature')
const signatureContext = signatureCanvas.getContext('2d')
signatureContext.lineCap = 'round';
signatureContext.strokeStyle = '#000000';
signatureContext.lineWidth = 1;


// load image
let originalFrontImage = new Image();
let originalBackImage = new Image();

originalFrontImage.src = '/static/img/front_body.png';
originalBackImage.src = '/static/img/back_body.png';

let frontImage = new Image();
let backImage = new Image();
frontImage.src = frontBackCanvas.frontDataUrl != "" ? frontBackCanvas.frontDataUrl : originalFrontImage.src;
backImage.src = frontBackCanvas.backDataUrl != "" ? frontBackCanvas.backDataUrl : originalBackImage.src;

frontImage.onload = function () {
    frontContext.drawImage(frontImage, 0, 0, 300, 600);
}

backImage.onload = function () {
    backContext.drawImage(backImage, 0, 0, 300, 600);
}

if (signature) {

    let signatureImage = new Image();
    signatureImage.src = signature

    signatureImage.onload = function () {
        signatureContext.drawImage(signatureImage, 0, 0, 300, 100)
    }

}

// initialize state 
let x = 0, y = 0;
let isMouseDown = false;
let isBack = false;
let isFront = false;
let isSignature = false;
let pointerAmount = []



const stopDrawing = () => {

    if (isMouseDown) {
        frontBackCanvas.backDataUrl = backCanvas.toDataURL()
        frontBackCanvas.frontDataUrl = frontCanvas.toDataURL()
        isMouseDown = false;
        if (isBack) {
            $("#id_area_of_soreness_back").val(frontBackCanvas.backDataUrl)
        } else if (isFront) {
            $("#id_area_of_soreness_front").val(frontBackCanvas.frontDataUrl)
        } else if (isSignature) {
            $("#id_signature").val(signatureCanvas.toDataURL())
        }
        isBack = false;
        isFront = false;
        isSignature = false;
        pointerAmount = [];






    }
}

const startDrawing = event => {
    isMouseDown = true;
    [x, y] = [event.offsetX, event.offsetY];
}

const drawingFront = event => {
    pointerAmount.push(event)

    let eventAmount = 0
    for (let i = 0; i < pointerAmount.length; i++) {
        if (event instanceof PointerEvent) {
            eventAmount++
        }
    }

    frontCanvas.style.touchAction = "None"
    isFront = true

}

const drawingBack = event => {
    pointerAmount.push(event)

    let eventAmount = 0
    for (let i = 0; i < pointerAmount.length; i++) {
        if (event instanceof PointerEvent) {
            eventAmount++
        }
    }


    backCanvas.style.touchAction = "None"
    isBack = true
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

        if (isFront) {
            context = frontContext
        } else if (isBack) {
            context = backContext
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


function clearFrontCanvas() {



    frontContext.clearRect(0, 0, 300, 600)
    frontContext.drawImage(originalFrontImage, 0, 0, 300, 600);

    frontBackCanvas.frontDataUrl = frontCanvas.toDataURL()
    $("#id_area_of_soreness_front").val("")
}

function clearBackCanvas() {

    backContext.clearRect(0, 0, 300, 600)
    backContext.drawImage(originalBackImage, 0, 0, 300, 600);
    frontBackCanvas.backDataUrl = backCanvas.toDataURL()
    $("#id_area_of_soreness_back").val("")
}

function clearSignatureCanvas() {
    signatureContext.clearRect(0, 0, 300, 100)
    $("#id_signature").val("")
}


frontCanvas.addEventListener('mousedown', startDrawing);
frontCanvas.addEventListener('mousedown', drawingFront);
frontCanvas.addEventListener('mousemove', drawLine);
frontCanvas.addEventListener('mouseup', stopDrawing);
frontCanvas.addEventListener('mouseout', stopDrawing);

backCanvas.addEventListener('mousedown', startDrawing);
backCanvas.addEventListener('mousedown', drawingBack);
backCanvas.addEventListener('mousemove', drawLine);
backCanvas.addEventListener('mouseup', stopDrawing);
backCanvas.addEventListener('mouseout', stopDrawing);

signatureCanvas.addEventListener('mousedown', startDrawing);
signatureCanvas.addEventListener('mousedown', drawingSignature);
signatureCanvas.addEventListener('mousemove', drawLine);
signatureCanvas.addEventListener('mouseup', stopDrawing);
signatureCanvas.addEventListener('mouseout', stopDrawing);

frontCanvas.addEventListener('pointerdown', startDrawing);
frontCanvas.addEventListener('pointerdown', drawingFront);
frontCanvas.addEventListener('pointermove', drawLine);
frontCanvas.addEventListener('pointerup', stopDrawing);
frontCanvas.addEventListener('pointerout', stopDrawing);

backCanvas.addEventListener('pointerdown', startDrawing);
backCanvas.addEventListener('pointerdown', drawingBack);
backCanvas.addEventListener('pointermove', drawLine);
backCanvas.addEventListener('pointerup', stopDrawing);
backCanvas.addEventListener('pointerout', stopDrawing);

signatureCanvas.addEventListener('pointerdown', startDrawing);
signatureCanvas.addEventListener('pointerdown', drawingSignature);
signatureCanvas.addEventListener('pointermove', drawLine);
signatureCanvas.addEventListener('pointerup', stopDrawing);
signatureCanvas.addEventListener('pointerout', stopDrawing);
