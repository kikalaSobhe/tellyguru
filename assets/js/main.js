const form = document.querySelector("#oracle-form");
const question = document.querySelector("#question");
const answer = document.querySelector("#answer");
const error = document.querySelector("#question-error");

const guidance = [
  "That sounds like a meeting that should have been an email.",
  "Make a smaller version first. The answer will become annoyingly obvious.",
  "Name the real problem. It is probably hiding behind the urgent one.",
  "Have lunch, then make one honest decision.",
  "Yes, but only if you can explain why in one sentence.",
  "I need more context. Suspiciously, this makes me sound professional.",
  "The complicated option has excellent marketing. Choose the clear one."
];

function guidanceFor(value) {
  const score = [...value.trim().toLowerCase()].reduce((total, character) => total + character.charCodeAt(0), 0);
  return guidance[score % guidance.length];
}

if (form && question && answer && error) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const value = question.value.trim();

    if (!value) {
      error.textContent = "The guru cannot answer a question you have not asked.";
      question.setAttribute("aria-invalid", "true");
      question.focus();
      return;
    }

    error.textContent = "";
    question.removeAttribute("aria-invalid");
    answer.classList.add("is-thinking");
    answer.setAttribute("aria-busy", "true");
    answer.querySelector("p").textContent = "Consulting the entirely unofficial archives...";

    window.setTimeout(() => {
      answer.querySelector("p").textContent = guidanceFor(value);
      answer.classList.remove("is-thinking");
      answer.removeAttribute("aria-busy");
    }, 480);
  });
}

const reveals = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.14 });

  reveals.forEach((element) => observer.observe(element));
} else {
  reveals.forEach((element) => element.classList.add("is-visible"));
}
