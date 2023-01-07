set -gx myterminal_editor nvim

alias c=clear
alias e=exit
alias H='cd ~/'
alias D='cd ~/Desktop'

alias df='df -h'
alias src-fish='source ~/.config/fish/config.fish'
alias nf='neofetch --config ~/.config/neofetch/configs/sm3.conf'

alias .kitty='$myterminal_editor ~/.config/kitty/'
alias .fish='$myterminal_editor ~/.config/fish/'
alias .nvim='$myterminal_editor ~/.config/nvim/'

alias aura.aur='sudo aura -Aacx'

alias nm.connect='nmcli c up Olive --ask'
alias list-installed-packages='pacman -Qi | awk \'/^Name/{name=$3} /^Installed Size/{print $4$5, name}\' | sort -h'
alias restart-sddm='sudo systemctl stop sddm && sudo systemctl start sddm'
