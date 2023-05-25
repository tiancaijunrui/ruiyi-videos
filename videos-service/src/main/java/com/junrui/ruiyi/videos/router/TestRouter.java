package com.junrui.ruiyi.videos.router;

import com.junrui.ruiyi.videos.handler.TestHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.server.RequestPredicates;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerResponse;

@Configuration
public class TestRouter {

    @Bean
    public RouterFunction<ServerResponse> testRouterFunction(TestHandler testHandler) {
        return RouterFunctions.nest(RequestPredicates.path("/test"),
                RouterFunctions.route(RequestPredicates.GET("/hello").and(RequestPredicates.accept(MediaType.APPLICATION_JSON)),
                        testHandler::hello)

        );
    }
}
