<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            body {
                /* margin: 0 auto; */
                background-color: teal;
                max-width: 800px;
                padding: 0 20px;
                font-family: Arial;
            }

            .chatbox {
                background-color: yellowgreen;
                float: left;
                width: 1000px;
                overflow-y: auto;
                height: 400px;
                padding: 0 20px;
                margin: 20px auto;
                border-radius: 5px;
            }

            .container {
                border: 2px solid #dedede;
                background-color: #f1f1f1;
                border-radius: 5px;
                padding: 10px;
                margin: 10px 0;
            }

            .darker {
                border-color: #ccc;
                background-color: #ddd;
            }

            .container::after {
                content: "";
                clear: both;
                display: table;
            }

            .container img {
                float: left;
                max-width: 60px;
                width: 100%;
                margin-right: 20px;
                border-radius: 50%;
            }

            .container img.right {
                float: right;
                margin-left: 20px;
                margin-right:0;
            }

            .container p.right {
                text-align: right;
            }
        </style>
    </head>
    <body>
        <h2>Chat Messages</h2>

        <div class="chatbox">
            <?php
                $chatLogFile = fopen("chatLog.txt", "r+");
                $chatLog = array();
                $shade = true;
                $i = 0;
                //Tampilkan chat yang telah ada
                while (!feof($chatLogFile)) {
                    if ($shade) {
                        array_push($chatLog, fgets($chatLogFile));
                        echo
                            "<div class=\"container\">
                                <img src=\"./images/bot.png\" alt=\"Bot\" style=\"width:100%;\">
                                <p>" . $chatLog[$i] . "</p>
                            </div>";
                        $i = $i + 1;
                    }
                    else {
                        array_push($chatLog, fgets($chatLogFile));
                        echo
                            "<div class=\"container darker\">
                                <img src=\"./images/user.png\" alt=\"User\" class =\"right\" style=\"width:100%;\">
                                <p class =\"right\">" . $chatLog[$i] . "</p>
                            </div>";
                            $i = $i + 1;
                    }
                    $shade = !$shade;
                }

                //Tampilkan pertanyaan pertama
                $choicesFile = fopen("choices.txt","r");
                while (!feof($choicesFile)){
                  //Ambil choices terakhir
                  $choice = intval(fgets($choicesFile));
                }
                fclose($choicesFile);

                //Cek apakah choice == -1
                if($choice == -1){
                  $output = "Halo! Panduan menggunakan: Masukkan angka 1 s.d. 3 untuk menggunakan algoritma 1: KMP, 2:BM, 3: Regex. Untuk mengganti algoritma yang digunakan, tulis 'ganti'";
                  array_push($chatLog, $output);
                  echo
                      "<div class=\"container\">
                          <img src=\"./images/bot.png\" alt=\"Bot\" style=\"width:100%;\">
                          <p>" . $output . "</p>
                      </div>";
                      fwrite($chatLogFile, "\n".trim($output));
                }

                fclose($chatLogFile);

                if (isset($_POST['chat'])) {
                    //Tulis ulang semua percakapan ke chatlog
                    $chatLogFile = fopen("chatLog.txt", "w");
                    $chat = $_POST['chat'];
                    for($num = 0; $num < count($chatLog); $num++)
                        fwrite($chatLogFile, $chatLog[$num]);
                    fwrite($chatLogFile, "\n".trim($chat));

                    //Tampilkan chat dari user
                    echo
                            "<div class=\"container darker\">
                                <img src=\"./images/user.png\" alt=\"User\" class =\"right\" style=\"width:100%;\">
                                <p class =\"right\">" . $chat . "</p>
                            </div>";

                    if(($choice == 0) || ($choice == -1)){
                        if((intval($chat) >= 1) && (intval($chat) <= 3)){
                            $choice = intval($chat);
                            if($choice == 1){
                              $output = "Silahkan tanyakan apa saja! *KMP*";
                            } else if($choice == 2){
                              $output = "Silahkan tanyakan apa saja! *BM*";
                            } else{ //choice == 3
                              $output = "Silahkan tanyakan apa saja! *Regex*";
                            }
                            $choicesFile = fopen("choices.txt","w");
                            fwrite($choicesFile, $choice);
                            fclose($choicesFile);

                            array_push($chatLog, $output);
                            echo
                                "<div class=\"container\">
                                    <img src=\"./images/bot.png\" alt=\"Bot\" style=\"width:100%;\">
                                    <p>" . $output . "</p>
                                </div>";
                        } else{
                          $output = "Input salah, masukkan angka 1 s.d. 3. 1: KMP, 2:BM, 3: Regex";
                          array_push($chatLog, $output);
                          echo
                              "<div class=\"container\">
                                  <img src=\"./images/bot.png\" alt=\"Bot\" style=\"width:100%;\">
                                  <p>" . $output . "</p>
                              </div>";
                        }
                        fwrite($chatLogFile, "\n".trim($output));
                    } else{
                      if($chat == "ganti"){
                        $choicesFile = fopen("choices.txt","w");
                        $output = "Halo! Panduan menggunakan: Masukkan angka 1 s.d. 3 untuk menggunakan algoritma 1: KMP, 2:BM, 3: Regex. Untuk mengganti algoritma yang digunakan, tulis 'ganti'";
                      //array_push($chatLog, $output);
                        echo
                            "<div class=\"container\">
                                <img src=\"./images/bot.png\" alt=\"Bot\" style=\"width:100%;\">
                                <p>" . $output . "</p>
                            </div>";
                            fwrite($chatLogFile, "\n".trim($output));
                        fwrite($choicesFile, "0");
                        fclose($choicesFile);
                      } else{

                        //Lakukan pattern matching sesuai $choice
                        //Debug
                        $cmd = "py Backend.py " . $choice;
                        $output = shell_exec($cmd);
                        //array_push($chatLog, $output);
                        echo
                            "<div class=\"container\">
                                <img src=\"./images/bot.png\" alt=\"Bot\" style=\"width:100%;\">
                                <p>" . $output . "</p>
                            </div>";
                        fwrite($chatLogFile, "\n".trim($output));
                      }
                    }
                  fclose($chatLogFile);
                }
            ?>
        </div>

        <form action="index.php" method="POST" style = "margin-left = 20px">
            <table border="0">
                <tr>
                    <td><input type="text" name="chat" size="30" /></td>
                    <td><input type="submit" value="Submit"/></td>
                </tr>
            </table>
        </form>

    </body>
</html>
