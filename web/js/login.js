async function login() {
  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: email.value,
      password: password.value
    })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail);
    return;
  }

  localStorage.setItem("token", data.access_token);
window.location.href = "/web/dashboard.html";
}
