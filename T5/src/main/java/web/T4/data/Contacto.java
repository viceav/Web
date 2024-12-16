package web.T4.data;

import java.sql.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Contacto {
  @Id
  private Integer id;

  private String email;

  @Column(name = "fecha_creacion")
  private Date fecha;

  public Integer getId() {
    return id;
  }

  public String getEmail() {
    return email;
  }

  public Date getFecha() {
    return fecha;
  }

}
