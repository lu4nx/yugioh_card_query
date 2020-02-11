current_dir=`pwd`
dst_file=/usr/bin/yugioh_card_query

pip3 install PyQt5

if [ ! -e ${dst_file} ]; then
    ln -s ${current_dir}/main.py /usr/bin/yugioh_card_query
fi

chmod +x /usr/bin/yugioh_card_query

cat > /usr/share/applications/yugioh_card_query.desktop <<EOF
[Desktop Entry]
Name=YuGiOh Card Query
Type=Application
Name[zh_CN]=游戏王离线查卡器
GenericName=YuGiOh Card Query
Comment=游戏王离线查卡器
Categories=Game;
Exec=/usr/bin/yugioh_card_query
Terminal=false
EOF
