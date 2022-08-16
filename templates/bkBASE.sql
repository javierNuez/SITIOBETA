-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-08-2022 a las 05:19:52
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sitiobeta`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_c` int(11) NOT NULL,
  `c_id_drogueria` int(11) NOT NULL,
  `c_cod_drogueria` int(11) NOT NULL,
  `c_desc_drogueria` text NOT NULL,
  `c_cuenta` text NOT NULL,
  `c_nombre` text NOT NULL,
  `c_cuit` text NOT NULL,
  `c_localidad` text NOT NULL,
  `c_postal` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_c`, `c_id_drogueria`, `c_cod_drogueria`, `c_desc_drogueria`, `c_cuenta`, `c_nombre`, `c_cuit`, `c_localidad`, `c_postal`) VALUES
(4, 50, 1, 'DROGUERIA DEL SUD (TODAS LAS SUCURSALES)', '1111', 'Farmacia', '343244', 'Burzaco', ''),
(5, 50, 1, 'DROGUERIA DEL SUD (TODAS)', '21231', 'Farmacia 123', '2333', 'Tres', ''),
(6, 49, 30018, 'CO.FA.RAL. (SALTA)', '4545', 'Otra Farmacia', '34534', 'Lomas', ''),
(8, 52, 30016, 'DROGUERIA DISVAL S.R.L.', '898', 'Una Farmacia', '8789', 'Monte Grande', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `droguerias`
--

CREATE TABLE `droguerias` (
  `id_d` int(11) NOT NULL,
  `d_cod` text NOT NULL,
  `d_descripcion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `droguerias`
--

INSERT INTO `droguerias` (`id_d`, `d_cod`, `d_descripcion`) VALUES
(48, '30017', 'ASOPROFARMA COOP. LTDA.'),
(49, '30018', 'CO.FA.RAL. (SALTA)'),
(50, '1', 'DROGUERIA DEL SUD (TODAS)'),
(51, '10', 'DROGUERIA SUIZO ARGENTINA (TODAS LAS SUCURSALES)'),
(52, '30016', 'DROGUERIA DISVAL S.R.L.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modulos`
--

CREATE TABLE `modulos` (
  `id_m` int(11) NOT NULL,
  `m_nombre` text NOT NULL,
  `m_titulo` text NOT NULL,
  `m_pie` text NOT NULL,
  `m_desde` date NOT NULL,
  `m_hasta` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `modulos`
--

INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`) VALUES
(1, 'Beta Clásico', 'Beta Clásico', 'Beta Clásico', '2022-08-11', '9999-12-31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ofertas`
--

CREATE TABLE `ofertas` (
  `id_o` int(11) NOT NULL,
  `o_modulo` text NOT NULL,
  `o_mod_nom` text NOT NULL,
  `o_mod_tit` text NOT NULL,
  `o_mod_pie` text NOT NULL,
  `o_mod_d` date NOT NULL,
  `o_mod_h` date NOT NULL,
  `o_producto` int(11) NOT NULL,
  `o_prod_cod` int(11) NOT NULL,
  `o_prod_des` text NOT NULL,
  `o_prod_d` date NOT NULL,
  `o_prod_h` date NOT NULL,
  `o_minima` int(11) NOT NULL,
  `o_descuento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ofertas`
--

INSERT INTO `ofertas` (`id_o`, `o_modulo`, `o_mod_nom`, `o_mod_tit`, `o_mod_pie`, `o_mod_d`, `o_mod_h`, `o_producto`, `o_prod_cod`, `o_prod_des`, `o_prod_d`, `o_prod_h`, `o_minima`, `o_descuento`) VALUES
(1, '1', 'Beta Clásico', 'Beta Clásico', 'Beta Clásico', '2022-08-11', '9999-12-31', 4, 5440, 'Oxa Gel 50mg', '2022-08-11', '9999-12-31', 4, 20),
(3, '1', 'Beta Clásico', 'Beta Clásico', 'Beta Clásico', '2022-08-11', '9999-12-31', 5, 5550, 'Oxa Prost', '2022-08-11', '9999-12-31', 5, 15);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_p` int(11) NOT NULL,
  `p_modulo` text NOT NULL,
  `p_mod_nom` text NOT NULL,
  `p_mod_tit` text NOT NULL,
  `p_mod_pie` text NOT NULL,
  `p_mod_d` date NOT NULL,
  `p_mod_h` date NOT NULL,
  `p_producto` int(11) NOT NULL,
  `p_prod_cod` int(11) NOT NULL,
  `p_prod_des` text NOT NULL,
  `p_prod_d` date NOT NULL,
  `p_prod_h` date NOT NULL,
  `p_minima` int(11) NOT NULL,
  `p_descuento` int(11) NOT NULL,
  `p_usuario` int(5) NOT NULL,
  `o_usuario_hash` int(14) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_p` int(11) NOT NULL,
  `p_cod` text NOT NULL,
  `p_descripcion` text NOT NULL,
  `p_desde` date NOT NULL,
  `p_hasta` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_p`, `p_cod`, `p_descripcion`, `p_desde`, `p_hasta`) VALUES
(4, '5440', 'Oxa Gel 50mg', '2022-08-11', '9999-12-31'),
(5, '5550', 'Oxa Prost', '2022-08-11', '9999-12-31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_u` int(11) NOT NULL,
  `u_nombre` text NOT NULL,
  `u_apellido` text NOT NULL,
  `u_rrdzz` int(5) NOT NULL,
  `u_mail` text NOT NULL,
  `u_desde` date NOT NULL,
  `u_hasta` date NOT NULL,
  `u_pass` text NOT NULL,
  `u_roll` text NOT NULL,
  `u_hash` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_u`, `u_nombre`, `u_apellido`, `u_rrdzz`, `u_mail`, `u_desde`, `u_hasta`, `u_pass`, `u_roll`, `u_hash`) VALUES
(56, 'Javier', 'Nuñez', 2588, 'jmn@betalab.com.ar', '2020-01-01', '9999-12-31', 'nun344', 'ADM', '70670623122588'),
(58, 'sup', 'sup', 1000, 'sup@sup.com', '2020-01-01', '9999-12-31', 'sup', 'SUP', '76084501451000');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_c`);

--
-- Indices de la tabla `droguerias`
--
ALTER TABLE `droguerias`
  ADD PRIMARY KEY (`id_d`);

--
-- Indices de la tabla `modulos`
--
ALTER TABLE `modulos`
  ADD PRIMARY KEY (`id_m`);

--
-- Indices de la tabla `ofertas`
--
ALTER TABLE `ofertas`
  ADD PRIMARY KEY (`id_o`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_p`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_p`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_u`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_c` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `droguerias`
--
ALTER TABLE `droguerias`
  MODIFY `id_d` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `modulos`
--
ALTER TABLE `modulos`
  MODIFY `id_m` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `ofertas`
--
ALTER TABLE `ofertas`
  MODIFY `id_o` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_p` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_p` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_u` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
