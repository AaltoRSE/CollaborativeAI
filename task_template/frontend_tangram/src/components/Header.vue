<template>
  <div class="header-container">
    <div class="header-content">
      <h1>🤖🤝🧑 Collaborative AI Arena</h1>
      <h2 :style="{ fontWeight: 'normal' }">
        Benchmarking collaborative capabilities of AI in the wild
      </h2>
    </div>
    <nav class="navbar">
      <a href="#">Home</a>
      <a href="#">Task</a>
      <a href="#">About Us</a>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Header"
}
</script>

<style scoped>
.header-container {
  background-color: rgb(76, 70, 163);
  color: white;
  display: flex;
  justify-content: space-between; 
  align-items: center; 
  height: 150px; 
  padding: 20px;
}

.navbar {
  color: white;
  display: flex;
  flex-direction: column;
}

.navbar a {
  padding: 5px;
}

a:link {
  color: white;
  background-color: transparent;
  text-decoration: none;
}

a:visited {
  color: white;
  background-color: transparent;
  text-decoration: none;
}

a:hover {
  color: red;
  background-color: transparent;
  text-decoration: underline;
}

a:active {
  color: yellow;
  background-color: transparent;
  text-decoration: underline;
}
</style>
