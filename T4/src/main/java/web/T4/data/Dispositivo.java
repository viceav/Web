package web.T4.data;

import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;

@Entity
public class Dispositivo {
  public enum Estado {
    FUNCIONA_PERFECTO,
    FUNCIONA_A_MEDIAS,
    NO_FUNCIONA
  }

  public enum Tipo {
    PANTALLA,
    NOTEBOOK,
    TABLET,
    CELULAR,
    CONSOLA,
    MOUSE,
    TECLADO,
    IMPRESORA,
    PARLANTE,
    AUDIFONOS,
    OTRO
  }

  @Id
  private Integer id;
  private Integer contacto_id;

  private String nombre;

  private String descripcion;

  @Enumerated(EnumType.STRING)
  private Tipo tipo;

  private Integer anos_uso;

  @Enumerated(EnumType.STRING)
  private Estado estado;

  private Integer contador_megusta;

  private Integer contador_nomegusta;

  public void setContador_megusta(Integer contador_megusta) {
    this.contador_megusta = contador_megusta;
  }

  public void setContador_nomegusta(Integer contador_nomegusta) {
    this.contador_nomegusta = contador_nomegusta;
  }

  public Integer getId() {
    return id;
  }

  public Integer getContacto_id() {
    return contacto_id;
  }

  public String getNombre() {
    return nombre;
  }

  public String getDescripcion() {
    return descripcion;
  }

  public Tipo getTipo() {
    return tipo;
  }

  public Integer getAnos_uso() {
    return anos_uso;
  }

  public Estado getEstado() {
    return estado;
  }

  public Integer getContador_megusta() {
    return contador_megusta;
  }

  public Integer getContador_nomegusta() {
    return contador_nomegusta;
  }

}
