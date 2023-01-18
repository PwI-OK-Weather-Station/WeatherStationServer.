<script>
    import { fetchPOST } from '../utils.js';
    import { authenticated, username, token } from '../store.js';
    async function login() {
    const json = await fetchPOST('/api/login', { email: $email, password: $password });
    if (json.username) {
      $username = json.name;
      $token = json.token
      $authenticated = true;
    } else {
      $authenticated = false;
    }
    message = json.message;
  }
</script>