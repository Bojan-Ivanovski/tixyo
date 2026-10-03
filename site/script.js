const copyButton = document.querySelector("[data-copy]");

copyButton?.addEventListener("click", async () => {
  const command = copyButton.dataset.copy;

  try {
    await navigator.clipboard.writeText(command);
    copyButton.textContent = "Copied";
    window.setTimeout(() => {
      copyButton.textContent = "Copy";
    }, 1600);
  } catch {
    copyButton.textContent = command;
  }
});
