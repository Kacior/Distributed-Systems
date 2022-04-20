package com.example.lab2_zad;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriBuilder;
import java.net.URI;


@Path("/hello")
public class RESTHelloWorldJava {
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String sayPlainTextHello() {
        return "Hello Jersey";
    }

    @GET
    @Produces(MediaType.TEXT_XML)
    public String sayXMLHello() {
        return "<?xml version=\"1.0\"?>" + "<hello> Hello Jersey" + "</hello>";
    }

    @GET
    @Produces(MediaType.TEXT_HTML)
    public String sayHtmlHello() {
        return "<html> " + "<title>" + "Hello Jersey" + "</title>" + "<body><h1>" + "Hello Jersey" + "</body></h1>" + "</html> ";
    }

    public static void main(String[] args) {
        Client client = ClientBuilder.newClient();
        WebTarget target= client.target(getBaseURI());

        System.out.println(target.path("rest").path("hello").request().accept(MediaType.TEXT_PLAIN).get(Response.class).toString());
        System.out.println(target.path("rest").path("hello").request().accept(MediaType.TEXT_PLAIN).get(String.class));
        System.out.println(target.path("rest").path("hello").request().accept(MediaType.TEXT_XML).get(String.class));
        System.out.println(target.path("rest").path("hello").request().accept(MediaType.TEXT_HTML).get(String.class));
    }

    private static URI getBaseURI() {return UriBuilder.fromUri("http://localhost:8080/lab2_zad").build();}
    }
