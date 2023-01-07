set ytdl_download_location $HOME/Videos/"%(title)s.%(ext)s"

function ytdl
  argparse u/url= res= l/list-formats -- $argv
  or return

  if set -q _flag_url
    if set -q _flag_l
      command yt-dlp -F $_flag_url
      and return
    end
    if set -q _flag_res
      set -l removeP (echo $_flag_res | sed 's/P//ig')
      command yt-dlp -S res:$removeP $_flag_url -o $ytdl_download_location
      and return
    end
    command yt-dlp $_flag_url -o $ytdl_download_location
  end
end
