<template>
  <footer className="footer-container">
    <div className="acknowledge-section">
      <h2>Acknowledgement</h2>
      <br></br>
      <p>Humane-AI Net (European project ….)</p>
      <p>AI Builder …</p>
      <p>placeholder</p>
    </div>
    <div className="bug-report-section">  
      <h2>Bug Report</h2>
      <br></br>
      <p>Report bugs to: <a href="mailto:bugs@example.com">xxx.yyy@aalto.fi</a></p>
    </div>
    <div className="terms-section">
      <h2>Terms of Service</h2>
      <br></br>
      <p>Read our <a href="/#">Terms of Service</a></p>
    </div>
    <div className="logo-section">
      <img src="../assets/image1.png" alt="Project Logo" />
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer"
}
</script>

<style scoped>
.footer-container {
  background-color: rgb(76, 70, 163);
  color: white;
  padding: 50px;
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
}

.footer-container h2,
.footer-container p {
  margin-bottom: 10px;
}

.footer-container h2 {
  font-size: 20px;
}

.acknowledge-section,
.bug-report-section,
.terms-section {
  flex: 1;
  margin-right: 20px;
  padding-right: 20px;
}

.logo-section img {
  width: 600px; 
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
