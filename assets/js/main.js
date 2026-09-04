const form = document.querySelector("#oracle-form");
const question = document.querySelector("#question");
const answer = document.querySelector("#answer");
const answerText = answer?.querySelector("p");
const error = document.querySelector("#question-error");
const bell = document.querySelector("#bell-stage");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

const verdicts = [
  "Cut the scope. Keep the standard.",
  "Name the decision. The rest is scenery.",
  "If nobody owns it, it is not a plan.",
  "Write the one-sentence version. Start there.",
  "Choose the answer you can still maintain next year.",
  "You already know. You are asking for permission.",
  "Ship the clear version. Improve the clever version later."
];

let typingTimer;

function verdictFor(value) {
  const score = [...value.trim().toLowerCase()].reduce((total, character) => total + character.charCodeAt(0), 0);
  return verdicts[score % verdicts.length];
}

function typeVerdict(text) {
  window.clearTimeout(typingTimer);

  if (!answerText || reducedMotion.matches) {
    if (answerText) answerText.textContent = text;
    return;
  }

  answerText.textContent = "";
  let index = 0;

  function typeNext() {
    answerText.textContent += text[index];
    index += 1;

    if (index < text.length) {
      typingTimer = window.setTimeout(typeNext, 22);
    }
  }

  typeNext();
}

if (form && question && answer && answerText && error) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const value = question.value.trim();

    if (!value) {
      error.textContent = "State the question first.";
      question.setAttribute("aria-invalid", "true");
      question.focus();
      return;
    }

    error.textContent = "";
    question.removeAttribute("aria-invalid");
    answer.classList.add("is-thinking");
    answer.setAttribute("aria-busy", "true");
    answerText.textContent = "The chair is considering...";

    if (bell) {
      bell.classList.remove("is-ringing");
      void bell.offsetWidth;
      bell.classList.add("is-ringing");
    }

    window.setTimeout(() => {
      answer.classList.remove("is-thinking");
      answer.removeAttribute("aria-busy");
      typeVerdict(verdictFor(value));
    }, reducedMotion.matches ? 0 : 420);
  });
}

const reveals = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window && !reducedMotion.matches) {
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
