<script language="Javascript">
function isUrlValid(str) {
 const pattern = new RegExp(
   '^(https?:\\/\\/)?' + // protocol
     '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
     '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR IP (v4) address
     '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
     '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
     '(\\#[-a-z\\d_]*)?$', // fragment locator
   'i'
 );
 return pattern.test(str);
}

document.writeln(isUrlValid('https://jionew.example:8080/')); // true
document.write(isUrlValid('mailto://example.com')); // false
</script>