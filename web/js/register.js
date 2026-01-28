async function register() {
  await fetch("/users/create", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      full_name: name.value,
      email: email.value,
      password: password.value,
      role_id: parseInt(role.value)
    })
  });
  alert("User created");
}
