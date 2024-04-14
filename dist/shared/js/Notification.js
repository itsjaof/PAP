const toast = document.querySelector(".toast")
const closeIcon = document.querySelector(".close")
const progress = document.querySelector(".progress")
let timer1, timer2

function sendNotification(type, text1, text2) {
  document.getElementById('text text-1').innerHTML = text1;
  document.getElementById('text text-2').innerHTML = text2;

  if(type === 'error') {
    const toastElement = document.getElementById("toast");
    const contentElement = document.getElementById("toast-content");
    const checkElement = document.getElementById("checkMark");
    const progressElement = document.getElementById("progress");

    toastElement.classList.add("errored");
    contentElement.classList.add("errored");
    progressElement.classList.add("errored");
    
    checkElement.classList.remove("fas", "fa-solid", "fa-check", "check");
    checkElement.classList.add("fa-solid", "fa-xmark", "errored");
  }

  toast.classList.add("active");
  progress.classList.add("active");

  timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 5000); //1s = 1000 milliseconds

  timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300);

  closeIcon.addEventListener("click", () => {
      toast.classList.remove("active");

      setTimeout(() => {
        progress.classList.remove("active");
      }, 300);
      clearTimeout(timer1);
      clearTimeout(timer2);
  });
}