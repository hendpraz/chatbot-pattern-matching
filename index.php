<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="HandheldFriendly" content="true">
        <link href="style.css" rel="stylesheet" type="text/css">
        <link rel="shortcut icon" href="./images/snowyOwl01.png" type="image/x-icon"/>
        <title>Chat with Fluffball</title>
    </head>
    
    <body>
        <h2 style = "color: white"><b>Chat with Fluffball</b></h2>

        <div class="chatbox" id="MainChatBox">
            <?php
                $chatLogFile = fopen("chatLog.txt", "r");
                $chatLog = array();
                $shade = true;
                $i = 0;

                // Tampilkan chat yang telah ada
                while (!feof($chatLogFile)) {
                    if ($shade) {
                        array_push($chatLog, fgets($chatLogFile));
                        ?>

                            <div class = "container darker">
                                <img src = "./images/SnowyOwlEye.gif" alt = "Bot">
                                <p> <?= $chatLog[$i]?> </p>
                            </div>

                        <?php
                        $i = $i + 1;
                    }
                    else {
                        array_push($chatLog, fgets($chatLogFile));
                        ?>

                            <div class = "container">
                                <img src = "./images/user.png" alt = "User" class = "right">
                                <p class = "right"> <?= $chatLog[$i]?> </p>
                            </div>

                        <?php
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
                    ?>

                        <div class = "container darker">
                            <img src = "./images/SnowyOwlEye.gif" alt = "Bot">
                            <p> <?= $output?> </p>
                        </div>

                    <?php
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
                    ?>

                        <div class = "container">
                            <img src = "./images/user.png" alt = "User" class = "right">
                            <p class = "right"> <?= $chat?> </p>
                        </div>

                    <?php

                    //Cek apakah pilihan algoritma sudah ada atau belum
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

                            ?>

                                <div class = "container darker">
                                    <img src = "./images/SnowyOwlTalk.gif" alt = "Bot">
                                    <p> <?= $output?> </p>
                                </div>

                            <?php

                        } else{
                            $output = "Input salah, masukkan angka 1 s.d. 3. 1: KMP, 2:BM, 3: Regex";
                            array_push($chatLog, $output);
                            ?>

                                <div class = "container darker">
                                    <img src = "./images/SnowyOwlTalk.gif" alt = "Bot">
                                    <p> <?= $output?> </p>
                                </div>

                            <?php
                        }
                        fwrite($chatLogFile, "\n".trim($output));
                    } else{
                        if($chat == "ganti"){
                            //ganti dengan algoritma lain
                            $choicesFile = fopen("choices.txt","w");
                            $output = "Masukkan angka 1 s.d. 3 untuk menggunakan algoritma 1: KMP, 2:BM, 3: Regex. Untuk mengganti algoritma yang digunakan, tulis 'ganti'";
                            //array_push($chatLog, $output);
                            ?>

                                <div class = "container darker">
                                    <img src = "./images/SnowyOwlTalk.gif" alt = "Bot">
                                    <p> <?= $output?> </p>
                                </div>

                            <?php
                            fwrite($chatLogFile, "\n".trim($output));
                            fwrite($choicesFile, "0");
                            fclose($choicesFile);
                            } else{

                            //Lakukan pattern matching sesuai $choice
                            //Debug
                            $cmd = "py Backend.py " . $choice;
                            $output = shell_exec($cmd);
                            //array_push($chatLog, $output);
                            ?>

                                <div class = "container darker">
                                    <img src = "./images/SnowyOwlTalk.gif" alt = "Bot">
                                    <p> <?= $output?> </p>
                                </div>

                            <?php
                            fwrite($chatLogFile, "\n".trim($output));
                        }
                    }

                    fclose($chatLogFile);
                }
            ?>
        </div>

        <div>
            <form action="index.php" method="POST" style = "margin-left = 200px">
                <table border="0">
                    <tr>
                        <td><input type="text" name="chat" size="100" placeholder = "Type your chat here" autofocus/></td>
                        <td><input type="submit" value="Send"/></td>
                    </tr>
                </table>
            </form>
        </div>

        <script type="text/javascript">
            function scrollDownChat() {
                var elmnt = document.getElementById("MainChatBox");
                elmnt.scrollTop = 9999999;
            }

            window.onload = scrollDownChat; 
        </script>
    </body>
</html>
