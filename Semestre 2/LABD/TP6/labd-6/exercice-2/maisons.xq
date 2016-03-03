declare variable $maisons := "maisons.xml" ;

<html>
  <body>
    <table border="1">
     <thead>
        <tr>
           <th>Maisons</th>
           <th>Surface m2</th>
        </tr>
     </thead>
     <tbody>

          {
          for $m in doc($maisons)//maison
          return
          <tr>
                <td> {$m/@id} </td>
                <td> {sum($m//*[not(ancestor::*/@surface-m2)]/@surface-m2)} </td>
          </tr>
          }

      </tbody>
    </table>
  </body>
</html>
