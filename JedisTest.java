import java.io.IOException;                                                    
import java.net.URI;
import java.net.URISyntaxException;
import java.util.HashMap;                                                      
import java.util.Map;                                                          
import java.util.List;                                                          
                                                                               
import redis.clients.jedis.BinaryJedis;                                        
import redis.clients.jedis.Jedis;                                              
import redis.clients.jedis.Protocol;                                           
import redis.clients.jedis.exceptions.JedisConnectionException;                
import redis.clients.jedis.exceptions.JedisDataException;                      
import redis.clients.util.SafeEncoder;    

public class JedisTest{
        public static void main(String[] args) throws JedisConnectionException, JedisDataException{
                Jedis jedis = new Jedis("localhost");
                String hashname = "sound";
                Map<String, String> decibels = jedis.hgetAll(hashname);
                System.out.println("Retrieved noise level: " );
                for (Map.Entry<String,String> baa : decibels.entrySet()){
                        String date = baa.getKey();
                        String noise = baa.getValue();
                        System.out.println("on " + date + ", noise was: " + noise);
                }
        }
}
