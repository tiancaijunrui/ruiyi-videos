package com.junrui.ruiyi.videos.common;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;

import net.bramp.ffmpeg.FFmpeg;

public class CommonAutoConfiguration {

    @Bean
    public FFmpeg ffmpeg(@Value("${ffmpeg.path}") String ffmpegPath) throws IOException {
        return new FFmpeg(ffmpegPath);
    }

}
