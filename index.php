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
                $chatLogFile = fopen("chatLog.txt", "r");
                $chatLog = array();
                $shade = true;
                $i = 0;

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

                fclose($chatLogFile);

                if (isset($_POST['chat'])) {
                    $chatLogFile = fopen("chatLog.txt", "w");

                    $chat = $_POST['chat'];
                    for($num = 0; $num < count($chatLog); $num++)
                        fwrite($chatLogFile, $chatLog[$num]);
                    fwrite($chatLogFile, "\n".$chat);

                    echo
                            "<div class=\"container darker\">
                                <img src=\"./images/user.png\" alt=\"User\" class =\"right\" style=\"width:100%;\">
                                <p class =\"right\">" . $chat . "</p>
                            </div>";
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
