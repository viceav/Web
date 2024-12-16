package web.T4.data;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Log {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Integer id;

  private String mensaje;

  public void setId(Integer id) {
    this.id = id;
  }

  public void setMensaje(String mensaje) {
    this.mensaje = mensaje;
  }
}
