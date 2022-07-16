function _setToastSession(type, options){
    sessionStorage.toastMsgs = JSON.stringify([{type:type, options:options}])
}

/**
 * These are new toast function, requires documentation. 
 */
function openErrorToast(options){
    const ERROR_TYPE = 2;
    if(options.timeout === undefined){
        options.timeout = 3000
    }

    if(options.redirect != undefined){
        _setToastSession(ERROR_TYPE, options)
        window.location.href = options.redirect
        return
    }

    var $globalWrappper = $("#_snf5-toast-message-global-wrapper")
    $globalWrappper.prepend(`
        <div id="${options.id?options.id:''}" class="_snf5-toast-outter-wrapper-error _snf5-toast-outter-wrapper">
            <div class="_snf5-toast-close-btn" onclick="_removeToast(this)"></div>

            <div class="_snf5-toast-inner-wrapper-error _snf5-toast-inner-wrapper">
                <svg version="1.1" viewBox="0 0 130.2 130.2">
                    <circle class="snf5-toast-path circle" fill="none" stroke="#D06079" stroke-width="6" stroke-miterlimit="10" cx="65.1" cy="65.1" r="62.1"/>
                    <line class="snf5-toast-path line" fill="none" stroke="#D06079" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" x1="34.4" y1="37.9" x2="95.8" y2="92.3"/>
                    <line class="snf5-toast-path line" fill="none" stroke="#D06079" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" x1="95.8" y1="38" x2="34.4" y2="92.2"/>
                </svg>
                <div class="_snf5-toast-message-wrapper">
                    <div class="_snf5-toast-message-header snf5-font snf5-font-12 snf5-semibold snf5-no-highlight">${options.title==undefined?"Error":options.title}</div>
                    <div class="_snf5-toast-message-paragraph snf5-font snf5-font-12 snf5-no-highlight">${options.message==undefined?"":options.message}</div>

                </div>
            </div>
        </div>
    `)

    var $toastMsg = $($globalWrappper.find("._snf5-toast-outter-wrapper-error")[0])
    var currentHeight = $toastMsg.css("height")
    $toastMsg.css("height", currentHeight)
   
    _setToastTimeoutEvent($toastMsg, options.timeout);
    $toastMsg.hover(_keepToastOpen, _timeoutToastClose)
}

function openSuccessToast(options){
    const SUCCESS_TYPE = 1;
    if(options.timeout === undefined){
        options.timeout = 3000
    }

    if(options.redirect != undefined){
        _setToastSession(SUCCESS_TYPE, options)
        window.location.href = options.redirect
        return
    }

    var $globalWrappper = $("#_snf5-toast-message-global-wrapper")
    $globalWrappper.prepend(`
        <div id="${options.id?options.id:''}" class="_snf5-toast-outter-wrapper-success _snf5-toast-outter-wrapper">
            <div class="_snf5-toast-close-btn" onclick="_removeToast(this)"></div>

            <div class="_snf5-toast-inner-wrapper-success _snf5-toast-inner-wrapper">
                <svg version="1.1" viewBox="0 0 130.2 130.2">
                    <circle class="snf5-toast-path circle" fill="none" stroke="#73AF55" stroke-width="6" stroke-miterlimit="10" cx="65.1" cy="65.1" r="62.1"/>
                    <polyline class="snf5-toast-path check" fill="none" stroke="#73AF55" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" points="100.2,40.2 51.5,88.8 29.8,67.5 "/>
                </svg>
                <div class="_snf5-toast-message-wrapper">
                    <div class="_snf5-toast-message-header snf5-font snf5-font-12 snf5-semibold snf5-no-highlight">${options.title==undefined?"Success":options.title}</div>
                    <div class="_snf5-toast-message-paragraph snf5-font snf5-font-12 snf5-no-highlight">${options.message==undefined?"":options.message}</div>

                </div>
            </div>
        </div>
    `)

    var $toastMsg = $($globalWrappper.find("._snf5-toast-outter-wrapper-success")[0])
    var currentHeight = $toastMsg.css("height")
    $toastMsg.css("height", currentHeight)
   
    _setToastTimeoutEvent($toastMsg, options.timeout);
    $toastMsg.hover(_keepToastOpen, _timeoutToastClose)
}

function openInfoToast(options){
    const INFO_TYPE = 3;
    if(options.timeout === undefined){
        options.timeout = 3000
    }

    if(options.redirect){
        _setToastSession(INFO_TYPE, options)
        window.location.href = options.redirect
        return
    }


    var $globalWrappper = $("#_snf5-toast-message-global-wrapper")
    $globalWrappper.prepend(`
        <div id="${options.id?options.id:''}" class="_snf5-toast-outter-wrapper-info _snf5-toast-outter-wrapper">
            <div class="_snf5-toast-close-btn" onclick="_removeToast(this)"></div>

            <div class="_snf5-toast-inner-wrapper-info _snf5-toast-inner-wrapper">

                <svg viewBox="0 0 55 55" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle class="snf5-toast-path circle" fill="none" stroke="#4680F7" stroke-width="2.8" stroke-miterlimit="10" cx="27" cy="25" r="25"/>
                    <path class="snf5-toast-path info" d="m 25.5166 21.9636 c 0.8127 0.1002 2.7752 0.8512 5.0489 -0.1166 c -0.443 0.3032 -1.9589 0.7463 -2.2619 2.2968 l -5.1478 12.436 c -1.7709 3.447 4.2059 3.1307 6.0717 0.0949" stroke="#4680F7" stroke-width="2.8"/>
                    <path class="snf5-toast-path line" d="M30.4315 12C28.9565 12 28.1821 12.7367 28.1821 14.0407C28.1739 14.3292 28.2268 14.6161 28.3374 14.8828C28.448 15.1494 28.6137 15.3897 28.8237 15.5878C29.0373 15.7918 29.2895 15.951 29.5657 16.0561C29.8418 16.1611 30.1362 16.2098 30.4315 16.1993C31.6926 16.1993 32.3858 15.4626 32.3858 14.1218C32.3858 12.7809 31.6926 12 30.4315 12Z" fill="#4680F7"/>
                </svg>

                <div class="_snf5-toast-message-wrapper">
                    <div class="_snf5-toast-message-header snf5-font snf5-font-12 snf5-semibold snf5-no-highlight">${options.title==undefined?"Info":options.title}</div>
                    <div class="_snf5-toast-message-paragraph snf5-font snf5-font-12 snf5-no-highlight">${options.message==undefined?"":options.message}</div>
                </div>

            </div>
        </div>
    `)

    var $toastMsg = $($globalWrappper.find("._snf5-toast-outter-wrapper-info")[0])
    var currentHeight = $toastMsg.css("height")
    $toastMsg.css("height", currentHeight)
   
    _setToastTimeoutEvent($toastMsg, options.timeout);
    $toastMsg.hover(_keepToastOpen, _timeoutToastClose)
}


function openLoadingToast(options){
    const LOADING_TYPE = 0;
    if(options.timeout === undefined){
        options.timeout = 3000
    }

    if(options.redirect){
        _setToastSession(LOADING_TYPE, options)
        window.location.href = options.redirect
        return
    }


    var $globalWrappper = $("#_snf5-toast-message-global-wrapper")
    $globalWrappper.prepend(`
        <div id="${options.id?options.id:''}" class="_snf5-toast-outter-wrapper-loading _snf5-toast-outter-wrapper">
            <div class="_snf5-toast-close-btn" onclick="_removeToast(this)"></div>
            <div class="_snf5-toast-inner-wrapper-loading _snf5-toast-inner-wrapper">
                <svg version="1.1" id="loader-1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 50 50" style="enable-background:new 0 0 50 50;" xml:space="preserve">
                    <path fill="#ED7E22" d="M25.251,6.461c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615V6.461z">
                        <animateTransform attributeType="xml" attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="0.6s" repeatCount="indefinite"></animateTransform>
                    </path>
                </svg>
                <div class="_snf5-toast-message-wrapper">
                    <div class="_snf5-toast-message-header snf5-font snf5-font-12 snf5-semibold snf5-no-highlight">${options.title==undefined?"Loading":options.title}</div>
                    <div class="_snf5-toast-message-paragraph snf5-font snf5-font-12 snf5-no-highlight">${options.message==undefined?"":options.message}</div>

                </div>
            </div>
        </div>
    `)

    var $toastMsg = $($globalWrappper.find("._snf5-toast-outter-wrapper-loading")[0])
    var currentHeight = $toastMsg.css("height")
    $toastMsg.css("height", currentHeight)

}

function removeToast(target){
    _setToastTimeoutEvent(target, timeout=0);
}





function _keepToastOpen(){
    var timerId =  $(this).attr('toast-timer-id')
    window.clearInterval(timerId)

}

function _timeoutToastClose(){

    var $toastMsg = $(this)
    _setToastTimeoutEvent($toastMsg, 2000);

}



function _setToastTimeoutEvent($toastMsg, timeout=3000){

    var id = setTimeout(function(){
        $toastMsg.css("opacity", 0)
        $toastMsg.css("height", 0)
        $toastMsg.css("margin", 0)
        setTimeout(function(){$toastMsg.remove()},1200)

    }, timeout)

    $toastMsg.attr('toast-timer-id', `${id}`)
}

function _removeToast(element){

    $this = $(element)
    if($this.attr("toast-timer-id")){
        window.clearInterval(timerId)
    }
    $toastMsg = $this.parent()

    $toastMsg.css("opacity", 0)
    $toastMsg.css("height", 0)
    $toastMsg.css("margin", 0)
    setTimeout(function(){$toastMsg.remove()},2000)

}


